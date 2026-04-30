# Dairy Herd Calendar & Weather Rules — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create `dairy_herd_calendar.json`, `dairy_weather_rules.json`, and their Markdown equivalents, then extend `evaluate_rules.py` to support dairy.

**Architecture:** Single-track (no breed filtering), Kenya seasons-first 12-month calendar. Rule engine extended with THI field, dairy stage tags, and dairy calendar activity handlers. ~49 rules across 9 categories. Full spec: `docs/superpowers/specs/2026-04-30-dairy-calendar-rules-design.md`. evaluate_rules LLD: `weather/docs/lld-evaluate-rules-dairy.md`.

**Tech Stack:** Python 3.11+, pytest, json (stdlib). Source PDFs in `weather/PDFs/Dairy/`.

---

## File Map

| Action | Path |
|--------|------|
| Create | `weather/rules/dairy/dairy_herd_calendar.json` |
| Create | `weather/rules/dairy/dairy_herd_calendar.md` |
| Create | `weather/rules/dairy/dairy_weather_rules.json` |
| Create | `weather/rules/dairy/dairy_weather_rules.md` |
| Modify | `weather/rules/evaluate_rules.py` |
| Create | `weather/tests/test_dairy.py` |

---

## Task 1: Directory setup and test scaffolding

**Files:**
- Create: `weather/rules/dairy/` (directory)
- Create: `weather/tests/test_dairy.py`

- [ ] **Step 1: Create directory**

```bash
mkdir -p /path/to/weather/rules/dairy
mkdir -p /path/to/weather/tests
```

- [ ] **Step 2: Create test file with structural tests (all will fail — files don't exist yet)**

Create `weather/tests/test_dairy.py`:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "rules"))

import pytest
from evaluate_rules import load_rules, load_calendar, evaluate_rules, parse_weather_data


# ── Calendar structural tests ─────────────────────────────────────────────────

def test_calendar_loads():
    calendar = load_calendar("dairy")
    assert "monthly_calendar" in calendar

def test_calendar_has_all_12_months():
    calendar = load_calendar("dairy")
    for m in range(1, 13):
        assert str(m) in calendar["monthly_calendar"], f"Month {m} missing"

def test_calendar_phenology_key_is_dairy():
    calendar = load_calendar("dairy")
    for m in range(1, 13):
        phenology = calendar["monthly_calendar"][str(m)]["phenology"]
        assert "Dairy" in phenology, f"Month {m} missing Dairy phenology key"

def test_calendar_phenology_values_are_valid():
    valid_stages = {
        "calving_season", "peak_lactation", "breeding_season",
        "late_lactation", "drying_off", "dry_period", "pre_calving"
    }
    calendar = load_calendar("dairy")
    for m in range(1, 13):
        stage = calendar["monthly_calendar"][str(m)]["phenology"]["Dairy"]
        assert stage in valid_stages, f"Month {m}: invalid stage '{stage}'"

def test_calendar_management_tasks_have_priority_and_action():
    calendar = load_calendar("dairy")
    for m in range(1, 13):
        tasks = calendar["monthly_calendar"][str(m)].get("management_tasks", {})
        for key, task in tasks.items():
            assert "priority" in task, f"Month {m}, task '{key}' missing priority"
            assert "action" in task, f"Month {m}, task '{key}' missing action"
            assert task["priority"] in ("critical", "high", "medium", "low"), \
                f"Month {m}, task '{key}' has invalid priority '{task['priority']}'"

def test_calendar_has_parasite_risk_not_pest_risk():
    calendar = load_calendar("dairy")
    for m in range(1, 13):
        month_data = calendar["monthly_calendar"][str(m)]
        assert "parasite_risk" in month_data, f"Month {m} missing parasite_risk"
        assert "pest_risk" not in month_data, f"Month {m} should not have pest_risk"


# ── Rules structural tests ────────────────────────────────────────────────────

def test_rules_load():
    rules = load_rules("dairy")
    assert "rules" in rules
    assert "metadata" in rules

def test_rules_count():
    rules = load_rules("dairy")
    assert len(rules["rules"]) >= 40, f"Expected ≥40 rules, got {len(rules['rules'])}"

def test_rules_have_required_fields():
    rules = load_rules("dairy")
    required = {"id", "category", "name", "weather_condition", "risk", "priority", "actions"}
    for rule in rules["rules"]:
        missing = required - set(rule.keys())
        assert not missing, f"Rule {rule.get('id', '?')} missing fields: {missing}"

def test_rule_ids_are_unique():
    rules = load_rules("dairy")
    ids = [r["id"] for r in rules["rules"]]
    assert len(ids) == len(set(ids)), "Duplicate rule IDs found"

def test_expected_categories_present():
    rules = load_rules("dairy")
    categories = {r["category"] for r in rules["rules"]}
    expected = {
        "HEAT_STRESS", "DISEASE_MASTITIS", "DISEASE_RESPIRATORY",
        "DISEASE_VECTOR", "PARASITES", "NUTRITION_FORAGE",
        "WATER", "REPRODUCTION", "SPRAYING"
    }
    missing = expected - categories
    assert not missing, f"Missing rule categories: {missing}"


# ── Rule trigger tests ────────────────────────────────────────────────────────

def _base_weather():
    """Minimal weather dict that won't trigger any rules on its own."""
    return {
        "temperature_c": 22, "temperature_max_c": 25, "temperature_min_c": 18,
        "temperature_change_24h_c": 2, "temperature_trend": "rising",
        "relative_humidity_pct": 60, "thi_value": 63,
        "wind_speed_kmh": 8, "wind_gust_kmh": 12,
        "cloud_cover_pct": 30, "qpf_today_mm": 0,
        "cumulative_rain_72h_mm": 0, "cumulative_rain_7d_mm": 0,
        "consecutive_dry_days": 3, "consecutive_wet_days": 0,
        "hours_since_last_rain": 72, "soil_temp_estimate_c": 20,
        "rain_probability_today_pct": 10, "rain_probability_next_6h_pct": 5,
        "rain_probability_next_12h_pct": 10,
        "is_daytime": True, "month": 7,
    }

def test_heat_stress_fires_at_thi_72():
    weather = {**_base_weather(), "thi_value": 74}
    rules = load_rules("dairy")
    triggered = evaluate_rules(weather, rules)
    assert any(r["category"] == "HEAT_STRESS" for r in triggered), \
        "Expected HEAT_STRESS rule at THI 74"

def test_heat_stress_does_not_fire_at_thi_65():
    weather = {**_base_weather(), "thi_value": 65}
    rules = load_rules("dairy")
    triggered = evaluate_rules(weather, rules)
    assert not any(r["category"] == "HEAT_STRESS" for r in triggered), \
        "HEAT_STRESS should not fire at THI 65"

def test_mastitis_risk_fires_in_wet_humid_conditions():
    weather = {**_base_weather(), "qpf_today_mm": 8, "relative_humidity_pct": 85}
    rules = load_rules("dairy")
    triggered = evaluate_rules(weather, rules)
    assert any(r["category"] == "DISEASE_MASTITIS" for r in triggered)

def test_respiratory_fires_on_cold_wind():
    weather = {**_base_weather(), "temperature_min_c": 10, "wind_speed_kmh": 22}
    rules = load_rules("dairy")
    triggered = evaluate_rules(weather, rules)
    assert any(r["category"] == "DISEASE_RESPIRATORY" for r in triggered)

def test_tick_vector_fires_after_rain():
    weather = {**_base_weather(), "cumulative_rain_72h_mm": 25, "temperature_c": 22}
    rules = load_rules("dairy")
    triggered = evaluate_rules(weather, rules)
    assert any(r["category"] == "DISEASE_VECTOR" for r in triggered)

def test_forage_scarcity_fires_after_dry_spell():
    weather = {**_base_weather(), "consecutive_dry_days": 25}
    rules = load_rules("dairy")
    triggered = evaluate_rules(weather, rules)
    assert any(r["category"] == "NUTRITION_FORAGE" for r in triggered)

def test_spraying_blocked_by_rain():
    weather = {**_base_weather(), "rain_probability_next_6h_pct": 50}
    rules = load_rules("dairy")
    triggered = evaluate_rules(weather, rules)
    assert any(r["category"] == "SPRAYING" for r in triggered)


# ── evaluate_rules.py extension tests ────────────────────────────────────────

def test_thi_computed_in_parse_weather_data():
    raw = {
        "wind": {"speed": {"value": 5}, "gust": {"value": 8}},
        "cloudCover": 40,
        "currentConditionsHistory": {
            "temperatureChange": {"degrees": 1.0},
            "maxTemperature": {"degrees": 28},
            "minTemperature": {"degrees": 20},
            "qpf": {"quantity": 0}
        }
    }
    parsed = parse_weather_data(raw)
    assert "thi_value" in parsed
    # T=24, RH=55 → THI = 0.8*24 + 0.55*(24-14.4) + 46.4 ≈ 71.7
    assert 60 < parsed["thi_value"] < 85

def test_dairy_stage_tags_enriched():
    from evaluate_rules import enrich_with_calendar
    weather = {"qpf_today_mm": 0, "wind_speed_kmh": 5}
    ctx = {"growth_stage": "calving_season", "season": "long_rains",
           "month_name": "March", "management_due": [], "disease_risk": {}, "pest_risk": {}}
    enriched = enrich_with_calendar(weather, ctx)
    assert "calving_season" in enriched["_active_stages"]

def test_avocado_still_works_after_dairy_changes():
    """Regression: avocado evaluation unchanged."""
    avocado_rules = load_rules("avocado")
    avocado_calendar = load_calendar("avocado")
    weather = {**_base_weather()}
    triggered = evaluate_rules(weather, avocado_rules, avocado_calendar, variety="Hass")
    assert isinstance(triggered, list)
```

- [ ] **Step 3: Run tests to confirm they all fail (files don't exist yet)**

```bash
cd weather && python -m pytest tests/test_dairy.py -v 2>&1 | head -40
```

Expected: All tests FAIL with `FileNotFoundError` or `KeyError`.

- [ ] **Step 4: Commit test scaffolding**

```bash
git add weather/tests/test_dairy.py
git commit -m "test: add dairy calendar and rule engine test scaffolding"
```

---

## Task 2: Extend evaluate_rules.py

**Files:**
- Modify: `weather/rules/evaluate_rules.py`

Full implementation details are in `weather/docs/lld-evaluate-rules-dairy.md`. Summary of 4 changes:

- [ ] **Step 1: Add THI derived field to `parse_weather_data()`**

In `parse_weather_data()`, after the `soil_temp_estimate_c` block (~line 369):

```python
if parsed.get("temperature_c") is not None and parsed.get("relative_humidity_pct") is not None:
    t = parsed["temperature_c"]
    rh = parsed["relative_humidity_pct"]
    parsed["thi_value"] = round(0.8 * t + (rh / 100) * (t - 14.4) + 46.4, 1)
```

- [ ] **Step 2: Add dairy stage tags to `enrich_with_calendar()`**

In `enrich_with_calendar()`, after the last existing stage tag block (before `weather["_active_stages"] = stage_tags`):

```python
if "calving" in stage:
    stage_tags.add("calving_season")
if "peak_lactation" in stage:
    stage_tags.add("peak_lactation")
if "breeding" in stage:
    stage_tags.add("breeding_season")
if "late_lactation" in stage:
    stage_tags.add("late_lactation")
if "drying_off" in stage:
    stage_tags.update(["late_lactation", "drying_off"])
if "dry_period" in stage:
    stage_tags.add("dry_period")
if "pre_calving" in stage:
    stage_tags.update(["dry_period", "pre_calving"])
```

- [ ] **Step 3: Add dairy activity handlers to `generate_calendar_rules()`**

Add 7 `elif` blocks before the final `else` (line ~253). Full code for each handler is in `weather/docs/lld-evaluate-rules-dairy.md` — Change 3. Handlers to add: `vaccination`, `deworming`, `acaricide_spraying`, `breeding_ai`, `drying_off`, `housing_maintenance`, `forage_planting`.

- [ ] **Step 4: Add `parasite_risk` alert and fix hardcoded disease alert text**

After the `high_risk_pests` block (~line 296), add the `parasite_risk` handling from LLD Change 4.

Replace the hardcoded avocado disease alert action:
```python
# OLD:
"Ensure fungicide program is current (copper every 14 days in wet weather)",
# NEW:
"Ensure current prevention program is active for flagged diseases",
```

- [ ] **Step 5: Run the three evaluate_rules.py extension tests**

```bash
cd weather && python -m pytest tests/test_dairy.py::test_thi_computed_in_parse_weather_data tests/test_dairy.py::test_dairy_stage_tags_enriched tests/test_dairy.py::test_avocado_still_works_after_dairy_changes -v
```

Expected: All 3 PASS.

- [ ] **Step 6: Commit**

```bash
git add weather/rules/evaluate_rules.py
git commit -m "feat: extend evaluate_rules.py for dairy (THI, stage tags, activity handlers)"
```

---

## Task 3: Create dairy_herd_calendar.json

**Files:**
- Create: `weather/rules/dairy/dairy_herd_calendar.json`

Source: Read `PDFs/Dairy/` — Handbook Ch 3 (breeds), Ch 4 (mastitis/feeding), ILRI Training Manual (calving, dry period, AI timing), Feeding Manual (rations, forage).

- [ ] **Step 1: Create the file with the skeleton and January data**

`weather/rules/dairy/dairy_herd_calendar.json` top-level structure:

```json
{
  "metadata": {
    "crop": "dairy",
    "version": "1.0",
    "last_updated": "2026-04-30",
    "description": "Monthly herd management calendar for Kenyan smallholder dairy farmers",
    "target_animal": "Friesian x Zebu crossbred (dominant smallholder type)",
    "sources": [
      "Dairy Farmers Handbook, 9th ed. 2025, Farmers Helping Farmers/UPEI",
      "Feeding Manual, ILRI/SDP/KDDP, 2007",
      "Smallholder Dairy Farmer Training Manual, ILRI Manual 24, 2016"
    ]
  },
  "kenya_seasons": {
    "long_rains":  { "months": [3, 4, 5], "description": "March–May" },
    "long_dry":    { "months": [6, 7, 8, 9], "description": "June–September" },
    "short_rains": { "months": [10, 11, 12], "description": "October–December" },
    "short_dry":   { "months": [1, 2], "description": "January–February" }
  },
  "animal_types": {
    "Dairy": {
      "description": "Kenya smallholder dairy cow — predominantly Friesian x Zebu crossbred",
      "breeds_covered": ["Holstein-Friesian", "Ayrshire", "Friesian x Zebu crossbred", "Jersey"],
      "calibrated_to": "Friesian x Zebu crossbred"
    }
  },
  "monthly_calendar": { ... },
  "herd_lifecycle_reference": { ... },
  "annual_input_schedule": { ... }
}
```

- [ ] **Step 2: Populate `monthly_calendar` for all 12 months**

Each month entry follows this schema:

```json
"1": {
  "month_name": "January",
  "season": "short_dry",
  "phenology": { "Dairy": "dry_period" },
  "management_tasks": {
    "housing_maintenance": {
      "priority": "critical",
      "action": "Inspect and repair housing before long rains — fix drainage, patch roof, top up bedding to 15cm"
    },
    "vaccination": {
      "priority": "high",
      "action": "Administer FMD booster and check Brucellosis vaccination records"
    },
    "deworming": {
      "priority": "high",
      "action": "Strategic deworming — dose by bodyweight (5mg/kg Albendazole or equivalent)"
    },
    "supplementary_feeding": {
      "priority": "high",
      "action": "Supplement dry cows with 2kg dairy meal/day and crop residues to maintain body condition score 3.0–3.5"
    }
  },
  "disease_risk": {
    "pneumonia": "medium",
    "mastitis": "low",
    "tick_borne_disease": "low"
  },
  "parasite_risk": {
    "ticks": "low",
    "internal_worms": "medium"
  },
  "nutrition_notes": "Short dry season — natural forage scarce. Supplement with crop residues (maize stover, bean haulms) and 2–3kg dairy meal for dry cows. Ensure adequate water supply."
}
```

Populate all 12 months using the seasonal rhythm from the spec:

| Month | Season | Phenology | Priority tasks |
|---|---|---|---|
| 1 (Jan) | short_dry | dry_period | housing_maintenance, vaccination, deworming, supplementary_feeding |
| 2 (Feb) | short_dry | pre_calving | pre_calving_management (critical), housing_prep, vaccination |
| 3 (Mar) | long_rains | calving_season | calving_management (critical), acaricide_spraying (critical), mastitis_monitoring |
| 4 (Apr) | long_rains | calving_season | acaricide_spraying (critical), mastitis_monitoring (critical), forage_management |
| 5 (May) | long_rains | peak_lactation | acaricide_spraying (critical), deworming, heat_stress_monitoring |
| 6 (Jun) | long_dry | peak_lactation | breeding_ai (critical), acaricide_spraying, forage_conservation |
| 7 (Jul) | long_dry | breeding_season | breeding_ai (critical), forage_conservation (critical), water_management |
| 8 (Aug) | long_dry | breeding_season | pregnancy_confirmation, forage_planting_prep, water_management (critical) |
| 9 (Sep) | long_dry | late_lactation | forage_planting (high), vaccination (annual FMD), housing_maintenance |
| 10 (Oct) | short_rains | drying_off | drying_off (critical), acaricide_spraying (critical), forage_planting |
| 11 (Nov) | short_rains | drying_off | dry_cow_management (critical), acaricide_spraying (critical), deworming |
| 12 (Dec) | short_rains | dry_period | housing_maintenance, vaccination (annual review), body_condition_scoring |

Disease risk follows tick seasons (high in Mar–May, Oct–Nov), mastitis risk follows wet seasons, heat stress peaks Jun–Aug.

- [ ] **Step 3: Populate `herd_lifecycle_reference`**

```json
"herd_lifecycle_reference": {
  "gestation_days": 282,
  "lactation_days": 305,
  "dry_period_days": { "min": 45, "max": 60, "recommended": 60 },
  "steaming_up_weeks_pre_calving": 3,
  "first_ai_days_post_calving": { "min": 50, "max": 80 },
  "peak_lactation_months_post_calving": { "min": 2, "max": 3 },
  "calving_interval_target_days": 365,
  "colostrum_feed_within_hours": 6,
  "dry_cow_therapy": "Infuse DCT antibiotic tubes at dry-off in all quarters"
}
```

- [ ] **Step 4: Populate `annual_input_schedule`**

```json
"annual_input_schedule": {
  "FMD_vaccination": { "months": [1, 9], "note": "Twice yearly — Jan and Sep" },
  "BQ_HS_vaccination": { "months": [2], "note": "Blackquarter + Haemorrhagic Septicaemia annually" },
  "brucellosis_check": { "months": [2], "note": "Annual check/certification" },
  "strategic_deworming": { "months": [1, 5, 11], "note": "3x per year at season transitions" },
  "acaricide_program": {
    "long_rains": { "months": [3, 4, 5], "frequency": "weekly" },
    "short_rains": { "months": [10, 11, 12], "frequency": "weekly" },
    "dry_seasons": { "months": [1, 2, 6, 7, 8, 9], "frequency": "fortnightly" }
  }
}
```

- [ ] **Step 5: Run calendar structural tests**

```bash
cd weather && python -m pytest tests/test_dairy.py::test_calendar_loads tests/test_dairy.py::test_calendar_has_all_12_months tests/test_dairy.py::test_calendar_phenology_key_is_dairy tests/test_dairy.py::test_calendar_phenology_values_are_valid tests/test_dairy.py::test_calendar_management_tasks_have_priority_and_action tests/test_dairy.py::test_calendar_has_parasite_risk_not_pest_risk -v
```

Expected: All 6 PASS.

- [ ] **Step 6: Commit**

```bash
git add weather/rules/dairy/dairy_herd_calendar.json
git commit -m "feat: add dairy herd management calendar (12-month, Kenya seasons)"
```

---

## Task 4: Create dairy_herd_calendar.md

**Files:**
- Create: `weather/rules/dairy/dairy_herd_calendar.md`

- [ ] **Step 1: Generate the Markdown from the JSON**

Mirror the structure of `weather/rules/avocado/avocado_crop_calendar.md`. The document should have:

1. Title + source attribution
2. Kenya seasons summary table
3. For each month: heading, season, phenology stage, management tasks table (priority | task | action), disease risk table, parasite risk table, nutrition notes
4. Herd lifecycle reference section (key constants)
5. Annual input schedule table

- [ ] **Step 2: Verify it renders (spot-check)**

```bash
# Check structure — should have 12 month headings
grep "^## " weather/rules/dairy/dairy_herd_calendar.md | wc -l
```

Expected: 12 (one per month)

- [ ] **Step 3: Commit**

```bash
git add weather/rules/dairy/dairy_herd_calendar.md
git commit -m "docs: add dairy herd calendar markdown for agronomist review"
```

---

## Task 5: Create dairy_weather_rules.json

**Files:**
- Create: `weather/rules/dairy/dairy_weather_rules.json`

Target: ~49 rules across 9 categories. All rules use weather fields from `parse_weather_data()` — see spec for the full field list. The `thi_value` field is now available after Task 2.

- [ ] **Step 1: Create file with metadata and empty rules array**

```json
{
  "metadata": {
    "crop": "dairy",
    "version": "1.0",
    "last_updated": "2026-04-30",
    "total_rules": 49,
    "categories": [
      "HEAT_STRESS", "DISEASE_MASTITIS", "DISEASE_RESPIRATORY",
      "DISEASE_VECTOR", "PARASITES", "NUTRITION_FORAGE",
      "WATER", "REPRODUCTION", "SPRAYING"
    ],
    "sources": [
      "Dairy Farmers Handbook, 9th ed. 2025, Farmers Helping Farmers/UPEI",
      "Feeding Manual, ILRI/SDP/KDDP, 2007",
      "Smallholder Dairy Farmer Training Manual, ILRI Manual 24, 2016"
    ]
  },
  "rules": []
}
```

- [ ] **Step 2: Add HEAT_STRESS rules (8 rules: HEAT-001 to HEAT-008)**

Each rule follows this structure:

```json
{
  "id": "HEAT-001",
  "category": "HEAT_STRESS",
  "name": "Mild heat stress — THI 72–77",
  "weather_condition": {
    "operator": "AND",
    "conditions": [
      { "field": "thi_value", "op": ">=", "value": 72 },
      { "field": "thi_value", "op": "<", "value": 78 }
    ]
  },
  "crop_context": { "applies_to_stages": ["all"] },
  "risk": "Mild heat stress reduces feed intake and milk yield by 5–10%. Reproduction efficiency drops.",
  "priority": "high",
  "actions": [
    "Ensure shade is available at all times — minimum 4 sq metres per cow",
    "Increase water access — cows drink 30L extra per day under heat stress",
    "Offer feed in cooler parts of the day (early morning and evening)",
    "Reduce concentrate ration slightly — high fermentation increases body heat"
  ],
  "preventive_actions": [
    "Plant shade trees in paddock",
    "Install shade structures over water troughs"
  ],
  "sources": ["Dairy Farmers Handbook, 9th ed. 2025, Ch. 5"]
}
```

Rules to add (HEAT-001 to HEAT-008):

| ID | Condition | Priority | Key action |
|---|---|---|---|
| HEAT-001 | THI 72–77 | high | Shade + extra water + cool-hour feeding |
| HEAT-002 | THI ≥ 78 | critical | Emergency cooling; expect 10–25% yield loss |
| HEAT-003 | THI ≥ 78 + month in [6,7,8] | critical | Delay AI or inseminate at 5am; conception drops 20–30% |
| HEAT-004 | temp_max > 32°C | high | Open housing ventilation; wet floor in extreme cases |
| HEAT-005 | temp_max > 32°C + relative_humidity > 70% | critical | Combined heat+humidity; evaporative cooling ineffective |
| HEAT-006 | THI ≥ 72 + consecutive_dry_days > 7 | high | Extended stress; monitor body condition scoring |
| HEAT-007 | THI ≥ 78 + month in [5,6,7] | critical | Peak lactation under severe stress — expect yield drop; contact vet |
| HEAT-008 | temperature_min > 22°C | medium | No overnight thermal recovery; cumulative stress building |

- [ ] **Step 3: Add DISEASE_MASTITIS rules (6 rules: MAST-001 to MAST-006)**

| ID | Condition | Priority | Key action |
|---|---|---|---|
| MAST-001 | qpf_today_mm > 5 + relative_humidity > 80 | high | Check housing drainage; replace wet bedding |
| MAST-002 | consecutive_wet_days > 3 | high | Daily udder hygiene; pre-dip + post-dip every milking |
| MAST-003 | temperature_change_24h_c > 6 + qpf_today > 3 | medium | Immune stress from weather change; monitor for new mastitis cases |
| MAST-004 | qpf > 5 + month in [10,11] (drying-off season) | critical | Highest mastitis risk at dry-off in wet conditions; DCT mandatory |
| MAST-005 | temperature_c BETWEEN 15–25 + relative_humidity > 85 | high | Environmental pathogen (Strep, E.coli) growth conditions |
| MAST-006 | qpf_today_mm > 10 | high | Inspect stall drainage immediately; mud at teat end |

- [ ] **Step 4: Add DISEASE_RESPIRATORY rules (6 rules: RESP-001 to RESP-006)**

| ID | Condition | Priority | Key action |
|---|---|---|---|
| RESP-001 | temperature_change_24h_c > 8 (falling) | critical | Sudden chill; check calves under 3 months immediately |
| RESP-002 | temperature_min < 12 + wind_speed > 15 | high | Wind-chill; close draught gaps in calf housing |
| RESP-003 | temperature_min < 12 + qpf_today > 2 | high | Wet + cold; dry calves; warm bedding |
| RESP-004 | temperature_min < 10 | medium | Close housing gaps; extra bedding for calves |
| RESP-005 | consecutive_dry_days > 14 + wind_speed > 20 | high | Dust pneumonia; wet down yards; reduce dust exposure |
| RESP-006 | qpf_today > 3 + wind_speed > 20 | high | Wet + wind; close ventilation openings on windward side |

Note on RESP-001: use `temperature_trend == "falling"` condition with `temperature_change_24h_c > 8`:
```json
"conditions": [
  { "field": "temperature_trend", "op": "==", "value": "falling" },
  { "field": "temperature_change_24h_c", "op": ">", "value": 8 }
]
```

- [ ] **Step 5: Add DISEASE_VECTOR rules (8 rules: VEC-001 to VEC-008)**

| ID | Condition | Priority | Key action |
|---|---|---|---|
| VEC-001 | cumulative_rain_72h > 20 + temp 15–30°C | critical | Tick activity elevated — ECF/anaplasmosis/babesiosis risk; spray within 48h |
| VEC-002 | consecutive_wet_days > 5 + temp > 15 | critical | High tick burden; increase acaricide to twice weekly |
| VEC-003 | cumulative_rain_72h > 30 + temp 20–30°C | critical | Peak vector conditions; check animals daily for ticks; treat immediately |
| VEC-004 | month in [3,4,5] + temp 18–28°C | high | Long rains tick season; weekly acaricide mandatory |
| VEC-005 | month in [10,11] + temp 18–28°C | high | Short rains tick season; resume weekly acaricide program |
| VEC-006 | cumulative_rain_72h > 10 + consecutive_dry_days was > 14 (use hours_since_last_rain > 336 + qpf_today > 5) | high | First rains after dry spell — tick larvae hatch; treat before infestation builds |
| VEC-007 | temp 15–30°C + relative_humidity > 70 + month in [3,4,5,10,11] | medium | Lumpy skin disease vector conditions; watch for LSD nodules |
| VEC-008 | cumulative_rain_7d_mm > 50 | medium | Stagnant water accumulation; remove pools near housing (vector breeding) |

For VEC-006, use:
```json
"conditions": [
  { "field": "hours_since_last_rain", "op": ">", "value": 336 },
  { "field": "qpf_today_mm", "op": ">", "value": 5 }
]
```

- [ ] **Step 6: Add PARASITES rules (4 rules: PARA-001 to PARA-004)**

| ID | Condition | Priority | Key action |
|---|---|---|---|
| PARA-001 | consecutive_dry_days > 30 | high | End of dry spell — strategic deworming before rains flush larvae |
| PARA-002 | cumulative_rain_72h > 15 + temperature > 18 | medium | Worm egg hatch conditions; check faecal egg count if possible |
| PARA-003 | month in [5,11] (post-rains) | medium | Post-rains strategic deworming window |
| PARA-004 | consecutive_wet_days > 7 + temperature 18–28°C | medium | Liver fluke (Fasciola) risk in waterlogged pastures |

- [ ] **Step 7: Add NUTRITION_FORAGE rules (6 rules: NUTR-001 to NUTR-006)**

| ID | Condition | Priority | Key action |
|---|---|---|---|
| NUTR-001 | consecutive_dry_days > 21 | high | Forage scarcity — increase dairy meal per milk formula: (milk kg − 5) ÷ 2 = kg meal/day |
| NUTR-002 | consecutive_dry_days > 42 | critical | Severe forage deficit — source emergency hay/silage; cows losing body condition |
| NUTR-003 | thi_value > 72 | medium | Heat reduces dry matter intake — offer high-quality forage; split concentrate into 3 feeds |
| NUTR-004 | consecutive_dry_days > 14 | medium | Start drawing down conserved forage (silage/hay); ration to last to next rains |
| NUTR-005 | qpf_today > 10 + consecutive_dry_days > 14 | medium | Rains returning — restock grazing rotation; rest paddocks 21 days |
| NUTR-006 | temperature_min < 12 | medium | Cold increases energy demand — add 10% to concentrate ration |

- [ ] **Step 8: Add WATER rules (4 rules: WATR-001 to WATR-004)**

| ID | Condition | Priority | Key action |
|---|---|---|---|
| WATR-001 | thi_value >= 72 | high | Water demand +30L/cow/day — ensure troughs refill within 1 hour |
| WATR-002 | thi_value >= 78 | critical | Provide cool water (< 20°C) — check temperature twice daily |
| WATR-003 | temperature_max > 32 | high | Peak demand 100L+ per cow — check trough flow rate |
| WATR-004 | consecutive_dry_days > 21 | high | Check water source levels; clean troughs of algae; borehole check |

- [ ] **Step 9: Add REPRODUCTION rules (4 rules: REPR-001 to REPR-004)**

| ID | Condition | Priority | Key action |
|---|---|---|---|
| REPR-001 | thi_value >= 78 + month in [6,7,8] | critical | Severe heat during AI window — inseminate at 5am; conception drops 20–30% |
| REPR-002 | temperature_min < 10 + month in [2,3] | critical | Cold at calving — dry calf immediately; ensure colostrum within 30 minutes |
| REPR-003 | qpf_today > 5 + temperature_min < 14 + month in [2,3] | critical | Wet + cold at calving — hypothermia risk; bring calf inside |
| REPR-004 | thi_value >= 72 + month in [6,7,8] | high | Heat stress during breeding — detect heat 3x daily; early morning insemination preferred |

- [ ] **Step 10: Add SPRAYING rules (3 rules: SPRY-001 to SPRY-003)**

| ID | Condition | Priority | Key action |
|---|---|---|---|
| SPRY-001 | rain_probability_next_6h > 40 | high | Delay acaricide application — product will wash off within 2 hours of rain |
| SPRY-002 | wind_speed > 15 | high | Wind drift — delay acaricide; poor coverage and operator exposure risk |
| SPRY-003 | qpf_today_mm > 2 | high | Rain today — acaricide wash-off risk; reschedule to next dry morning |

- [ ] **Step 11: Update `total_rules` in metadata to match actual count**

```bash
python3 -c "
import json
with open('weather/rules/dairy/dairy_weather_rules.json') as f:
    d = json.load(f)
d['metadata']['total_rules'] = len(d['rules'])
print(f'Total rules: {len(d[\"rules\"])}')
with open('weather/rules/dairy/dairy_weather_rules.json', 'w') as f:
    json.dump(d, f, indent=2)
"
```

- [ ] **Step 12: Run rules structural tests**

```bash
cd weather && python -m pytest tests/test_dairy.py::test_rules_load tests/test_dairy.py::test_rules_count tests/test_dairy.py::test_rules_have_required_fields tests/test_dairy.py::test_rule_ids_are_unique tests/test_dairy.py::test_expected_categories_present -v
```

Expected: All 5 PASS.

- [ ] **Step 13: Run rule trigger tests**

```bash
cd weather && python -m pytest tests/test_dairy.py::test_heat_stress_fires_at_thi_72 tests/test_dairy.py::test_heat_stress_does_not_fire_at_thi_65 tests/test_dairy.py::test_mastitis_risk_fires_in_wet_humid_conditions tests/test_dairy.py::test_respiratory_fires_on_cold_wind tests/test_dairy.py::test_tick_vector_fires_after_rain tests/test_dairy.py::test_forage_scarcity_fires_after_dry_spell tests/test_dairy.py::test_spraying_blocked_by_rain -v
```

Expected: All 7 PASS.

- [ ] **Step 14: Commit**

```bash
git add weather/rules/dairy/dairy_weather_rules.json
git commit -m "feat: add dairy weather rules (49 rules, 9 categories)"
```

---

## Task 6: Create dairy_weather_rules.md

**Files:**
- Create: `weather/rules/dairy/dairy_weather_rules.md`

- [ ] **Step 1: Generate the Markdown**

Mirror `weather/rules/avocado/avocado_weather_rules.md`. Structure:

1. Title + source attribution + total rule count
2. For each category: `## CATEGORY_NAME (N rules)` heading, then a table with columns: ID | Name | Trigger condition | Priority | Key actions
3. Notes section: THI formula, field reference, how to read the rules

- [ ] **Step 2: Spot-check**

```bash
grep "^## " weather/rules/dairy/dairy_weather_rules.md
```

Expected: 9 lines (one per category).

- [ ] **Step 3: Commit**

```bash
git add weather/rules/dairy/dairy_weather_rules.md
git commit -m "docs: add dairy weather rules markdown for agronomist review"
```

---

## Task 7: Full test run

- [ ] **Step 1: Run complete test suite**

```bash
cd weather && python -m pytest tests/test_dairy.py -v
```

Expected: All tests PASS.

- [ ] **Step 2: Smoke test the rule engine end-to-end**

```bash
cd weather/rules && python evaluate_rules.py
```

Expected: Avocado advisory prints without error (regression check).

- [ ] **Step 3: Quick dairy smoke test**

```bash
cd weather/rules && python3 -c "
from evaluate_rules import load_rules, load_calendar, evaluate_rules
import json

rules = load_rules('dairy')
calendar = load_calendar('dairy')

# Simulate hot dry July afternoon
weather = {
    'temperature_c': 29, 'temperature_max_c': 33, 'temperature_min_c': 22,
    'temperature_change_24h_c': 2, 'temperature_trend': 'rising',
    'relative_humidity_pct': 65, 'thi_value': 74,
    'wind_speed_kmh': 10, 'wind_gust_kmh': 15,
    'cloud_cover_pct': 20, 'qpf_today_mm': 0,
    'cumulative_rain_72h_mm': 0, 'cumulative_rain_7d_mm': 0,
    'consecutive_dry_days': 25, 'consecutive_wet_days': 0,
    'hours_since_last_rain': 600, 'soil_temp_estimate_c': 27,
    'rain_probability_today_pct': 5, 'rain_probability_next_6h_pct': 5,
    'rain_probability_next_12h_pct': 10,
    'is_daytime': True, 'month': 7,
}

triggered = evaluate_rules(weather, rules, calendar, variety='Dairy')
print(f'Rules triggered: {len(triggered)}')
for r in triggered:
    print(f'  [{r[\"priority\"]:>13}] {r[\"id\"]:>12} — {r[\"name\"]}')
"
```

Expected: 5–12 rules triggered, mix of HEAT_STRESS, NUTRITION_FORAGE, WATER, SPRAYING categories.

- [ ] **Step 4: Final commit if any fixups were needed**

```bash
git add -p  # stage only if there are fixups
git commit -m "fix: dairy rule engine integration fixes from smoke test"
```
