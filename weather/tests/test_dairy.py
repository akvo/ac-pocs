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
        "cumulative_rain_24h_mm": 0, "cumulative_rain_72h_mm": 0, "cumulative_rain_7d_mm": 0,
        "consecutive_dry_days": 3, "consecutive_wet_days": 0, "consecutive_dry_hours": 72,
        "hours_since_last_rain": 72, "soil_temp_estimate_c": 20,
        "rain_probability_today_pct": 10, "rain_probability_next_6h_pct": 5,
        "rain_probability_next_12h_pct": 10,
        "is_daytime": True, "is_early_morning_or_late_evening": False,
        "month": 7, "hour": 10,
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
