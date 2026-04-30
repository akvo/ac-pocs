# LLD: Extending `evaluate_rules.py` for Dairy

## Context

`evaluate_rules.py` already supports multiple crops via the `crop` parameter in `load_rules()` and `load_calendar()`. The core evaluation logic (`evaluate_rule_conditions`, `evaluate_condition`, `filter_rules_by_growth_stage`, `prioritize_and_resolve`) is fully generic and requires **no changes**.

Dairy requires 4 targeted additions:

| # | What | Where | Why |
|---|------|--------|-----|
| 1 | THI derived field | `parse_weather_data()` | Dairy heat stress rules use THI, not raw temperature |
| 2 | Dairy stage tags | `enrich_with_calendar()` | Stage-to-tag mapping is hardcoded to avocado stages |
| 3 | Dairy activity handlers | `generate_calendar_rules()` | Dairy calendar tasks need weather-gated logic |
| 4 | `parasite_risk` support | `generate_calendar_rules()` | Dairy uses `parasite_risk`, not `pest_risk` |

---

## Change 1 — THI Derived Field

**File:** `evaluate_rules.py`  
**Function:** `parse_weather_data()`  
**Where:** After the `soil_temp_estimate_c` block (~line 369)

THI (Temperature-Humidity Index) is the standard measure for dairy heat stress. Thresholds:
- THI < 72: comfortable
- THI 72–78: mild stress (reduced feed intake, slightly lower yield)
- THI ≥ 78: severe stress (conception rates drop 20–30%, yield drops significantly)

Formula: `THI = 0.8 × T + (RH / 100) × (T − 14.4) + 46.4`

```python
# Add immediately after soil_temp_estimate_c
if parsed.get("temperature_c") is not None and parsed.get("relative_humidity_pct") is not None:
    t = parsed["temperature_c"]
    rh = parsed["relative_humidity_pct"]
    parsed["thi_value"] = round(0.8 * t + (rh / 100) * (t - 14.4) + 46.4, 1)
```

Dairy weather rules will reference `thi_value` as a field, e.g.:
```json
{ "field": "thi_value", "op": ">=", "value": 72 }
```

---

## Change 2 — Dairy Stage Tags

**File:** `evaluate_rules.py`  
**Function:** `enrich_with_calendar()`  
**Where:** After the existing stage tag block (after line 101, before `weather["_active_stages"] = stage_tags`)

The dairy calendar uses `"phenology": {"Dairy": "<stage_name>"}`. Stage names used in the dairy calendar are:

| Calendar phenology value | Stage tags to add |
|--------------------------|-------------------|
| `calving_season` | `calving_season` |
| `peak_lactation` | `peak_lactation` |
| `breeding_season` | `breeding_season` |
| `late_lactation` | `late_lactation` |
| `drying_off` | `late_lactation`, `drying_off` |
| `dry_period` | `dry_period` |
| `pre_calving` | `dry_period`, `pre_calving` |

Add the following block. It sits alongside the existing avocado mappings — they don't conflict because avocado stages never contain "calving", "lactation", etc.

```python
# Dairy stage tags — add after the existing avocado stage tag blocks
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

Dairy weather rules will use `applies_to_stages` values from the table above, e.g.:
```json
"crop_context": { "applies_to_stages": ["breeding_season"] }
```

---

## Change 3 — Dairy Activity Handlers

**File:** `evaluate_rules.py`  
**Function:** `generate_calendar_rules()`  
**Where:** Insert as new `elif` blocks before the final `else` block (currently at line 253)

The dairy herd calendar uses these activity keys in `management_tasks`. Each needs weather-gated logic:

| Activity key | Weather gate | Effect |
|---|---|---|
| `vaccination` | Dry day preferred | Post-injection infection risk in wet |
| `deworming` | No gate — always fire | Strategic timing; note dosing requirement |
| `acaricide_spraying` | No rain, wind < 15 km/h | Product wash-off/drift |
| `breeding_ai` | THI check | Conception rate drops at THI ≥ 78 |
| `drying_off` | No gate — always fire | Dry cow therapy reminder |
| `housing_maintenance` | Rain increases urgency | Wet housing drives mastitis |
| `forage_planting` | Rain > 2mm preferred | Dry-soil establishment failure |

Add these `elif` blocks:

```python
elif activity == "vaccination":
    if rain < 2:
        rules.append({
            "id": f"CAL-{activity.upper()}",
            "category": "CALENDAR_MANAGEMENT",
            "name": "Calendar: Vaccination due — suitable conditions today",
            "priority": priority,
            "risk": "none — dry conditions reduce post-injection site infection",
            "actions": [action, "Record all animals vaccinated with date and batch number"],
            "source": "crop_calendar",
        })
    else:
        rules.append({
            "id": f"CAL-{activity.upper()}-WAIT",
            "category": "CALENDAR_MANAGEMENT",
            "name": "Calendar: Vaccination due — wait for dry day",
            "priority": "informational",
            "risk": "Wet conditions increase post-injection infection risk",
            "actions": [action, "Wait for dry conditions before vaccinating"],
            "source": "crop_calendar",
        })

elif activity == "deworming":
    rules.append({
        "id": f"CAL-{activity.upper()}",
        "category": "CALENDAR_MANAGEMENT",
        "name": "Calendar: Strategic deworming due this month",
        "priority": priority,
        "risk": "Internal parasites peak after rains — treat before worm load builds",
        "actions": [
            action,
            "Weigh animals first — dose by bodyweight, not estimate",
            "Record product name, dose, and animals treated",
        ],
        "source": "crop_calendar",
    })

elif activity == "acaricide_spraying":
    wind = weather.get("wind_speed_kmh", 0)
    if rain < 2 and wind < 15:
        rules.append({
            "id": f"CAL-{activity.upper()}",
            "category": "CALENDAR_MANAGEMENT",
            "name": "Calendar: Acaricide treatment due — good window today",
            "priority": priority,
            "risk": "none — dry, calm conditions for acaricide application",
            "actions": [
                action,
                "Ensure full body coverage including ears, tail base, and udder",
                "Rotate acaricide class every 3 months to prevent tick resistance",
            ],
            "source": "crop_calendar",
        })
    else:
        rules.append({
            "id": f"CAL-{activity.upper()}-WAIT",
            "category": "CALENDAR_MANAGEMENT",
            "name": "Calendar: Acaricide treatment due — wait for dry, calm day",
            "priority": "informational",
            "risk": "Rain washes off acaricide; wind causes drift and missed coverage",
            "actions": [action, f"Today: {rain}mm rain, {wind}km/h wind — delay until conditions improve"],
            "source": "crop_calendar",
        })

elif activity == "breeding_ai":
    thi = weather.get("thi_value", 65)
    if thi >= 78:
        rules.append({
            "id": f"CAL-{activity.upper()}-HEAT",
            "category": "CALENDAR_MANAGEMENT",
            "name": "Calendar: AI breeding window — heat stress reducing conception risk",
            "priority": "high",
            "risk": f"THI {thi} (≥78) — conception rates drop 20–30% under severe heat stress",
            "actions": [
                action,
                "If possible, schedule AI for early morning when THI is lowest",
                "Ensure shade and cool water to reduce cow stress before insemination",
            ],
            "source": "crop_calendar",
        })
    else:
        rules.append({
            "id": f"CAL-{activity.upper()}",
            "category": "CALENDAR_MANAGEMENT",
            "name": "Calendar: AI breeding window — conditions suitable",
            "priority": priority,
            "risk": "none — THI within acceptable range for AI",
            "actions": [
                action,
                "Check for standing heat 2–3 times daily (morning, midday, evening)",
                "Inseminate 12–18 hours after standing heat is first observed",
            ],
            "source": "crop_calendar",
        })

elif activity == "drying_off":
    rules.append({
        "id": f"CAL-{activity.upper()}",
        "category": "CALENDAR_MANAGEMENT",
        "name": "Calendar: Dry-off period — cows due for drying off this month",
        "priority": priority,
        "risk": "Inadequate dry period reduces next lactation yield and raises mastitis risk",
        "actions": [
            action,
            "Infuse dry cow therapy (DCT) antibiotic tubes at dry-off",
            "Check udder daily for first 2 weeks after dry-off for mastitis signs",
            "Reduce feed to low-energy ration to support milk let-down cessation",
        ],
        "source": "crop_calendar",
    })

elif activity == "housing_maintenance":
    if rain > 0:
        rules.append({
            "id": f"CAL-{activity.upper()}-URGENT",
            "category": "CALENDAR_MANAGEMENT",
            "name": "Calendar: Housing maintenance — wet conditions increase urgency",
            "priority": "high",
            "risk": "Wet, dirty housing is the leading driver of mastitis and respiratory disease in dairy",
            "actions": [
                action,
                "Fix drainage channels before rains continue — standing water must not pool in stalls",
                "Add dry bedding (sawdust or dry grass) over wet floor",
                "Check roof for leaks and repair",
            ],
            "source": "crop_calendar",
        })
    else:
        rules.append({
            "id": f"CAL-{activity.upper()}",
            "category": "CALENDAR_MANAGEMENT",
            "name": "Calendar: Housing maintenance — schedule now before rains",
            "priority": priority,
            "risk": "none — proactive maintenance while conditions are dry",
            "actions": [
                action,
                "Check and clear drainage channels",
                "Inspect roof, repair before short rains begin",
                "Top up bedding depth to 10–15cm",
            ],
            "source": "crop_calendar",
        })

elif activity == "forage_planting":
    if rain > 2:
        rules.append({
            "id": f"CAL-{activity.upper()}",
            "category": "CALENDAR_MANAGEMENT",
            "name": "Calendar: Forage planting window — rain providing good establishment",
            "priority": priority,
            "risk": "none — rain-assisted planting conditions",
            "actions": [
                action,
                "Plant Napier grass cuttings or seed Boma Rhodes/Brachiaria while soil is moist",
                "Apply basal fertiliser (DSP) at planting into moist soil",
            ],
            "source": "crop_calendar",
        })
    else:
        rules.append({
            "id": f"CAL-{activity.upper()}-WAIT",
            "category": "CALENDAR_MANAGEMENT",
            "name": "Calendar: Forage planting window — prepare land, plant on first rain",
            "priority": "informational",
            "risk": "Planting into dry soil causes poor germination and establishment failure",
            "actions": [
                action,
                "Prepare land and source planting material now",
                "Plant within 3 days of first significant rain (>5mm)",
            ],
            "source": "crop_calendar",
        })
```

---

## Change 4 — `parasite_risk` Support in Disease/Pest Alerts

**File:** `evaluate_rules.py`  
**Function:** `generate_calendar_rules()`  
**Where:** After the existing `high_risk_pests` block (~line 296)

The dairy calendar uses `parasite_risk` (e.g., ticks, worms) as a key, not `pest_risk`. Add handling alongside the existing pest alert:

```python
# Add after the existing pest_risk block
parasite_risk = calendar_ctx.get("parasite_risk", {})
high_risk_parasites = [p for p, level in parasite_risk.items() if level in ("high", "very_high")]
if high_risk_parasites:
    rules.append({
        "id": "CAL-PARASITE-ALERT",
        "category": "CALENDAR_MANAGEMENT",
        "name": "Calendar: Elevated parasite risk this month",
        "priority": "high" if any(parasite_risk[p] == "very_high" for p in high_risk_parasites) else "medium",
        "risk": f"Seasonal parasite pressure elevated for: {', '.join(high_risk_parasites)}",
        "actions": [
            f"Increase monitoring frequency for {', '.join(high_risk_parasites)}",
            "Check animals for tick attachment sites (ears, tail, udder, groin)",
            "Assess faecal egg count before strategic deworming if possible",
        ],
        "source": "crop_calendar",
    })
```

Also update the existing `CAL-DISEASE-ALERT` block (line ~278) to remove the avocado-specific action. Replace:
```python
"Ensure fungicide program is current (copper every 14 days in wet weather)",
```
With:
```python
"Ensure current prevention program is active for flagged diseases",
```

---

## How to Call for Dairy

No change to call sites. The caller loads dairy-specific files and passes `variety="Dairy"`:

```python
rules_data = load_rules("dairy")       # loads rules/dairy/dairy_weather_rules.json
calendar   = load_calendar("dairy")    # loads rules/dairy/dairy_herd_calendar.json

triggered = evaluate_rules(
    weather,
    rules_data,
    calendar,
    variety="Dairy",        # single track — matches phenology key in the calendar
)
triggered = prioritize_and_resolve(triggered, rules_data)
```

The dairy calendar JSON must use `"Dairy"` as the phenology key:
```json
"phenology": {
    "Dairy": "calving_season"
}
```

---

## Testing Checklist

After implementing the changes, verify:

```python
# 1. THI field is computed
weather = {"temperature_c": 28, "relative_humidity_pct": 80, ...}
parsed = parse_weather_data(raw)
assert "thi_value" in parsed
assert parsed["thi_value"] >= 72   # hot + humid should be stress

# 2. Dairy stage tags are mapped
# Simulate a calendar context with calving_season phenology
# then call enrich_with_calendar and check _active_stages
weather["growth_stage"] = "calving_season"
weather = enrich_with_calendar(weather, {"growth_stage": "calving_season", ...})
assert "calving_season" in weather["_active_stages"]

# 3. HEAT_STRESS rule fires at THI ≥ 72
weather = {"thi_value": 74, "month": 3, ...}
triggered = evaluate_rules(weather, rules_data, calendar, variety="Dairy")
assert any(r["id"] == "HEAT-001" for r in triggered)

# 4. HEAT_STRESS rule does not fire at THI 65
weather = {"thi_value": 65, "month": 3, ...}
triggered = evaluate_rules(weather, rules_data, calendar, variety="Dairy")
assert not any(r["id"] == "HEAT-001" for r in triggered)

# 5. breeding_ai calendar rule carries heat warning at THI ≥ 78
weather = {"thi_value": 80, "qpf_today_mm": 0, ...}
cal_rules = generate_calendar_rules(
    {"management_due": [{"activity": "breeding_ai", "priority": "high", "action": "Schedule AI this month"}]},
    weather
)
assert any(r["id"] == "CAL-BREEDING_AI-HEAT" for r in cal_rules)

# 6. acaricide_spraying calendar rule is blocked by rain
weather = {"qpf_today_mm": 5, "wind_speed_kmh": 5, ...}
cal_rules = generate_calendar_rules(
    {"management_due": [{"activity": "acaricide_spraying", "priority": "critical", "action": "Spray for ticks"}]},
    weather
)
assert any(r["id"] == "CAL-ACARICIDE_SPRAYING-WAIT" for r in cal_rules)

# 7. Avocado rules still work after dairy additions (regression)
avocado_rules = load_rules("avocado")
avocado_calendar = load_calendar("avocado")
triggered = evaluate_rules(weather, avocado_rules, avocado_calendar, variety="Hass")
assert isinstance(triggered, list)
```

---

## Files Not Changed

These files are generic and require no modification:

- `evaluate_rule_conditions()` — operator logic is data-driven
- `evaluate_condition()` — field/op/value evaluation is generic
- `filter_rules_by_growth_stage()` — reads `applies_to_stages` from the rule JSON
- `prioritize_and_resolve()` — priority ordering is shared across all crops
- `load_rules()` / `load_calendar()` — already multi-crop via the `crop` parameter

---

## Summary of Lines Modified

| Function | Change type | Approx lines added |
|---|---|---|
| `parse_weather_data` | Add THI block | +5 |
| `enrich_with_calendar` | Add dairy stage tags | +12 |
| `generate_calendar_rules` | Add 7 dairy activity handlers | +90 |
| `generate_calendar_rules` | Add `parasite_risk` alert block | +15 |
| `generate_calendar_rules` | Fix hardcoded avocado disease alert text | −1 / +1 |
| **Total** | | **~120 lines** |
