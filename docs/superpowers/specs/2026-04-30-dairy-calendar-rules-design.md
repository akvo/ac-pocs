# Dairy Herd Calendar & Weather Rules — Design Spec

**Date:** 2026-04-30  
**Project:** Weather Advisory System — Dairy extension  
**Status:** Awaiting implementation

---

## What We Are Building

A dairy herd management calendar and a set of weather-triggered advisory rules for Kenyan smallholder dairy farmers, equivalent in structure to the existing avocado and potato rule sets.

**Outputs:**
- `rules/dairy/dairy_herd_calendar.json` — 12-month herd management calendar
- `rules/dairy/dairy_herd_calendar.md` — human-readable version for agronomist review
- `rules/dairy/dairy_weather_rules.json` — weather-triggered advisory rules
- `rules/dairy/dairy_weather_rules.md` — human-readable version for agronomist review

**Sources:** Three PDFs in `PDFs/Dairy/`:
- *Dairy Farmers Handbook* (9th ed., 2025) — Farmers Helping Farmers / UPEI
- *Feeding Manual* (ILRI/SDP/KDDP, 2007)
- *Smallholder Dairy Farmer Training Manual* (ILRI Manual 24, 2016)

---

## Design Decisions

### Single animal track

The farmer profile only captures `dairy_farmer: true` — no breed is recorded. The calendar and rules use a single track calibrated to the dominant smallholder animal type described in the PDFs: the **Friesian × Zebu crossbred**. Where thresholds differ by breed (e.g. heat stress), the conservative value for the more sensitive exotic/crossbred type is used, which also protects hardier local breeds.

The dairy calendar uses `"Dairy"` as its single phenology key, matching the `variety="Dairy"` call in the rule engine — structurally identical to avocado's `variety="Hass"`.

### Kenya seasons-first calendar

The calendar is organised month-by-month, anchored to Kenya's bimodal rainfall pattern — the same structure as avocado and potato. It is not organised around the lactation cycle (which is cow-individual and unknown to the system).

Seasonal rhythm:
- **Long Rains (Mar–May):** calving peak, rising lactation, high tick and mastitis risk
- **Long Dry (Jun–Sep):** peak lactation, AI/breeding window, forage thinning
- **Short Rains (Oct–Dec):** late lactation, drying-off, second tick season
- **Short Dry (Jan–Feb):** dry period management, steaming-up, housing maintenance

### No changes to core rule engine

`evaluate_rule_conditions`, `evaluate_condition`, `filter_rules_by_growth_stage`, and `prioritize_and_resolve` are fully generic and unchanged. See `weather/docs/lld-evaluate-rules-dairy.md` for the 4 targeted additions to `evaluate_rules.py` required to support dairy (~120 lines total).

---

## Calendar Structure

Mirrors `avocado_crop_calendar.json` exactly. Top-level sections:

```
metadata
kenya_seasons
animal_types          ← replaces "varieties"; single entry: "Dairy"
monthly_calendar
  [1..12]
    month_name
    season
    phenology
      Dairy: <stage>  ← single key; stage values listed below
    management_tasks
      <activity>
        priority      ← critical | high | medium | low
        action
    disease_risk
      <disease>: <level>   ← very_high | high | medium | low
    parasite_risk           ← replaces "pest_risk" for dairy
      <parasite>: <level>
    nutrition_notes
herd_lifecycle_reference    ← reference constants, not calendar-driven
annual_input_schedule       ← vaccines, deworming, acaricide by month
```

### Phenology stage values (used as `applies_to_stages` in rules)

| Stage value | Months (typical) | Description |
|---|---|---|
| `calving_season` | Mar–Apr | Calving peak; cows transitioning to lactation |
| `peak_lactation` | May–Jul | Maximum milk yield; highest nutritional demand |
| `breeding_season` | Jun–Aug | AI window timed to calve at next long rains |
| `late_lactation` | Aug–Sep | Declining yield; body condition recovery |
| `drying_off` | Oct–Nov | Cessation of milking; dry cow therapy |
| `dry_period` | Nov–Jan | Rest period; disease monitoring; housing prep |
| `pre_calving` | Feb–Mar | Steaming-up; transition feeding; calving prep |

### Management task activity keys

These keys are recognised by `generate_calendar_rules()` in the rule engine:

| Key | Trigger condition |
|---|---|
| `vaccination` | Dry day preferred |
| `deworming` | Always fires; note bodyweight dosing |
| `acaricide_spraying` | Blocked by rain or wind > 15 km/h |
| `breeding_ai` | Heat-warning added at THI ≥ 78 |
| `drying_off` | Always fires; dry cow therapy reminder |
| `housing_maintenance` | Urgency escalated when raining |
| `forage_planting` | Gated on rain > 2mm; land prep advice if dry |

---

## Weather Rules Structure

Mirrors `avocado_weather_rules.json`. Each rule has:

```json
{
  "id": "HEAT-001",
  "category": "HEAT_STRESS",
  "name": "...",
  "weather_condition": {
    "operator": "AND",
    "conditions": [
      { "field": "thi_value", "op": ">=", "value": 72 }
    ]
  },
  "crop_context": {
    "applies_to_stages": ["all"]
  },
  "risk": "...",
  "priority": "high",
  "actions": [...],
  "preventive_actions": [...],
  "sources": [...]
}
```

### Rule categories and expected rule count

| Category | Rules | Key weather fields used |
|---|---|---|
| `HEAT_STRESS` | ~8 | `thi_value` (≥72 mild, ≥78 severe) |
| `DISEASE_MASTITIS` | ~6 | `qpf_today_mm`, `relative_humidity_pct`, `temperature_c` |
| `DISEASE_RESPIRATORY` | ~6 | `temperature_min_c`, `wind_speed_kmh`, `qpf_today_mm`, `temperature_change_24h_c` |
| `DISEASE_VECTOR` | ~8 | `cumulative_rain_72h_mm`, `temperature_c`, `consecutive_wet_days` |
| `PARASITES` | ~4 | `consecutive_dry_days`, `cumulative_rain_72h_mm` |
| `NUTRITION_FORAGE` | ~6 | `consecutive_dry_days`, `temperature_max_c`, `thi_value` |
| `WATER` | ~4 | `thi_value`, `consecutive_dry_days`, `temperature_max_c` |
| `REPRODUCTION` | ~4 | `thi_value`, `temperature_min_c` |
| `SPRAYING` | ~3 | `rain_probability_next_6h_pct`, `wind_speed_kmh` |
| **Total** | **~49** | |

### Key thresholds (from PDF sources)

| Condition | Threshold | Source |
|---|---|---|
| Mild heat stress | THI ≥ 72 | Dairy Farmers Handbook |
| Severe heat stress | THI ≥ 78 | Dairy Farmers Handbook |
| Mastitis risk (wet housing) | Rain > 5mm + RH > 80% | ILRI Training Manual |
| Calf pneumonia risk | Temp drop > 5°C overnight OR wind > 20 km/h + rain | Dairy Farmers Handbook |
| Tick activity (ECF risk) | Cumulative rain 72h > 20mm + temp 15–30°C | Dairy Farmers Handbook |
| Forage scarcity | Consecutive dry days > 21 | Feeding Manual |
| AI conception drop | THI ≥ 78 | Smallholder Training Manual |

### New derived weather field: `thi_value`

THI is required for the HEAT_STRESS and REPRODUCTION categories. It must be computed in `parse_weather_data()`:

```
THI = 0.8 × T + (RH / 100) × (T − 14.4) + 46.4
```

Where T = `temperature_c`, RH = `relative_humidity_pct`. See LLD for implementation.

---

## Integration with Existing Pipeline

No changes to the pipeline or farmer profile. The call sequence for dairy is identical to avocado:

```python
rules_data = load_rules("dairy")
calendar   = load_calendar("dairy")
weather    = parse_weather_data(raw_forecast)

triggered  = evaluate_rules(weather, rules_data, calendar, variety="Dairy")
triggered  = prioritize_and_resolve(triggered, rules_data)
```

The `advisory_prompt.txt` template is crop-agnostic and works unchanged for dairy — triggered rules and calendar context are injected the same way.

---

## Files to Produce

| File | Format | Notes |
|---|---|---|
| `rules/dairy/dairy_herd_calendar.json` | JSON | 12 months, single Dairy track |
| `rules/dairy/dairy_herd_calendar.md` | Markdown | For agronomist review |
| `rules/dairy/dairy_weather_rules.json` | JSON | ~49 rules across 9 categories |
| `rules/dairy/dairy_weather_rules.md` | Markdown | For agronomist review |

---

## What Is Not in Scope

- Breed-specific rule filtering — not possible without breed in farmer profile
- Lactation-cycle-first calendar — not possible without individual cow records
- Individual cow health tracking — the advisory is broadcast, not per-animal
- Feed ration calculator — advisory only; ration calculation is a separate tool
