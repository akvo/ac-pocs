# Kenya Dairy Weather Advisory Rules

**For agronomist review**  
Version 1.0 | 30 April 2026 | 49 rules across 9 categories

This document describes the weather-triggered advisory rules used by our system to generate recommendations for dairy farmers in Kenya. Each rule monitors specific weather conditions and, when triggered, produces actionable advice. Please review for agronomic accuracy.

**Sources referenced throughout:**
- **Dairy Farmers Handbook, 9th ed. 2025** — Farmers Helping Farmers/UPEI
- **Feeding Manual** — ILRI/SDP/KDDP (2007)
- **Smallholder Dairy Farmer Training Manual** — ILRI Manual 24 (2016)

**Priority levels used:**

| Priority | Meaning |
|---|---|
| Critical | Immediate action required — significant animal loss or production collapse possible |
| High | Action needed within 24–48 hours |
| Medium | Monitor and act within the week |
| Low | Awareness — act when convenient |
| Informational | No action needed — background knowledge |

---

## HEAT_STRESS (8 rules)

| ID | Name | Trigger Condition | Priority | Key Actions |
|---|---|---|---|---|
| HEAT-001 | Mild heat stress — THI 72–77 | THI ≥ 72 AND < 78 | High | Provide ≥4 sq m shade/cow; increase water 30 L/day; move feeding to early morning (5–7 am) & evening (after 6 pm); ensure good ventilation |
| HEAT-002 | Severe heat stress — THI ≥ 78 | THI ≥ 78 | Critical | Emergency cooling: shade immediately; wet cows with cool water & use fans; provide 100+ L/cow cool water continuously; feed only during coolest hours (4–7 am, after 7 pm); delay AI; expect 15–25% milk loss |
| HEAT-003 | Severe heat stress in peak dry season — THI ≥ 78, June–August | THI ≥ 78 AND month in [6,7,8] | Critical | Emergency cooling measures; draw on silage/hay reserves; provide 100+ L/cow/day water; delay all AI until September; increase dairy meal: (milk kg − 5) ÷ 2 = kg meal/day; monitor for heat exhaustion (rectal temp > 40°C) |
| HEAT-004 | High daytime temperature — max > 32°C | Max temp > 32°C | High | Move afternoon milking to before 1 pm; provide ≥4 sq m shade/cow; ensure 100 L/cow/day water availability; reduce herd density in afternoon; check freshly calved & high-yielders |
| HEAT-005 | High temperature combined with humidity — max > 32°C & RH > 70% | Max temp > 32°C AND RH > 70% | Critical | Emergency cooling: wet cows with cool water; maximize airflow & fans essential; provide 100+ L/cow/day cool water, change twice daily if possible; delay AI, embryo transfers & stressful procedures; watch for panting/off-feed; call vet if rectal temp > 40.5°C |
| HEAT-006 | Heat stress compounded by dry spell — THI ≥ 72 & dry > 7 days | THI ≥ 72 AND consecutive dry days > 7 | High | Check all water sources (troughs, tanks, streams); begin drawing on hay/silage reserves; provide shade & ensure ventilation; increase dairy meal: (milk kg − 5) ÷ 2 = kg meal/day; monitor BCS—do not lose more than 0.5 score/month |
| HEAT-007 | Severe heat stress at start of long dry season — THI ≥ 78, May–July | THI ≥ 78 AND month in [5,6,7] | Critical | Activate silage & hay reserves immediately; emergency cooling (shade, wetting, fans); provide 100+ L/cow/day water; delay AI & breeding; increase dairy meal; monitor all cows daily—prioritize high-yielders & freshly calved |
| HEAT-008 | Warm nights — minimum temperature > 22°C | Min temp > 22°C | Medium | Ensure maximum overnight ventilation; check water troughs full before sunset; consider early morning milking (4–5 am); monitor cumulative milk loss—3+ warm nights = take action |

---

## DISEASE_MASTITIS (6 rules)

| ID | Name | Trigger Condition | Priority | Key Actions |
|---|---|---|---|---|
| MAST-001 | Mastitis risk — rain & high humidity | Rain today > 5 mm AND RH > 80% | High | Check housing drainage—no pooling; add dry bedding (≥10 cm depth); apply teat pre-dip AND post-dip at every milking; check udders daily for swelling/heat/clots; dry off any cow showing mastitis signs after consulting vet |
| MAST-002 | Mastitis risk — extended wet period (> 3 consecutive wet days) | Consecutive wet days > 3 | High | Bring cows into housing during heavy rain; replace all wet bedding with dry material; apply teat pre & post-dip at every milking—iodine-based post-dip most effective; inspect teats for wet chapping; conduct CMT (California Mastitis Test) this week |
| MAST-003 | Mastitis risk — sudden temperature change with rain | Temp change 24h > 6°C AND rain today > 3 mm | Medium | Shelter cows from rain & cold wind—close windward side; maintain rigorous pre-dip & post-dip routine; watch for off-feed or udder swelling in next 48 hours; ensure dry, warm resting area |
| MAST-004 | Dry-off mastitis risk — rain during October–November | Rain today > 5 mm AND month in [10,11] | Critical | Apply dry cow therapy (DCT) antibiotic tubes at dry-off—mandatory in wet conditions; apply teat sealant after DCT to block teat orifice; inspect udder daily for 2 weeks post dry-off; keep dry cows in well-bedded housing, not wet paddock; maintain pre-dip & post-dip at last milking before dry-off |
| MAST-005 | Mastitis risk — cool moist conditions (15–25°C, RH > 85%) | Temp 15–25°C AND RH > 85% | High | Maintain strict pre-dip & post-dip at every milking—do not skip; increase bedding replacement frequency; check teat condition—soft, wet skin increases infection risk; conduct CMT on all cows this week; ensure milking equipment functioning correctly |
| MAST-006 | Mastitis risk — heavy rainfall (> 10 mm today) | Rain today > 10 mm | High | Keep cows under cover during & immediately after heavy rain; clean teats with individual disposable wipes before milking—no shared cloth; apply teat pre-dip & post-dip at every milking; clear drainage channels; add dry bedding after rain stops |

---

## DISEASE_RESPIRATORY (6 rules)

| ID | Name | Trigger Condition | Priority | Key Actions |
|---|---|---|---|---|
| RESP-001 | Respiratory disease alert — rapid temperature drop | Temp trend falling AND temp change 24h > 8°C | Critical | Check all calves immediately—BRD kills calves within 24–48 hours if untreated; close all draughts in calf housing; add extra dry bedding; monitor adult cows for coughing/nasal discharge; separate sick calves immediately; check calf temp (< 38°C = hypothermia risk) |
| RESP-002 | Calf cold & respiratory risk — cold night with wind (min < 12°C, wind > 15 km/h) | Min temp < 12°C AND wind speed > 15 km/h | High | Block draughts at calf level with boards/sacking; add extra dry bedding—above knees; consider calf jackets for calves < 2 weeks old; check colostrum records; close windward side of adult housing |
| RESP-003 | Calf pneumonia risk — cold night with rain (min < 12°C, rain > 2 mm) | Min temp < 12°C AND rain today > 2 mm | High | Ensure all calves housed & dry overnight—bring outdoor calves inside; dry any wet calves with towel (wet calves lose heat 5x faster); check for respiratory signs: cough, nasal discharge, fast breathing (> 30 breaths/min), off feed; call vet immediately if symptoms present; close rain-facing openings |
| RESP-004 | Cold stress risk — minimum temperature below 10°C | Min temp < 10°C | Medium | Check all calves for early respiratory signs: cough, snotty nose, dullness, off feed; ensure ≥15 cm dry bedding depth, changed every 3–4 days; increase milk/replacer feeding by 10%; vaccinate unvaccinated calves for IBR & PI-3; block windward openings at calf height |
| RESP-005 | Dusty conditions respiratory risk — extended dry spell with wind (dry > 14 days, wind > 20 km/h) | Consecutive dry days > 14 AND wind speed > 20 km/h | High | Wet down housing area & paddock entrances to reduce dust; ensure cattle not fed dry hay in dusty conditions—soak hay first; ensure adequate airflow without creating draughts; watch for increased coughing/nasal discharge |
| RESP-006 | Respiratory risk — rain with wind (rain > 3 mm, wind > 20 km/h) | Rain today > 3 mm AND wind speed > 20 km/h | High | Bring calves < 3 months old inside immediately; close windward side of all housing to block driving rain; check freshly calved cows & high-yielders—most susceptible; dry any wet calves with towels; monitor for coughing & nasal discharge over next 24–48 hours |

---

## DISEASE_VECTOR (8 rules)

| ID | Name | Trigger Condition | Priority | Key Actions |
|---|---|---|---|---|
| VEC-001 | Tick-borne disease risk — rain & warm temperatures (72h rain > 20 mm, temp 15–30°C) | 72h rain > 20 mm AND temp 15–30°C | Critical | Spray all cattle with acaricide within 48 hours—do not delay; check all cattle daily for tick attachment sites; record tick burden score (0–5) per animal; watch for ECF signs 2–4 weeks later: swollen lymph nodes, high fever (>40°C), off feed; remove engorged ticks by hand from sensitive areas |
| VEC-002 | Tick & fly vector alert — extended wet period & warmth (wet days > 5, temp > 15°C) | Consecutive wet days > 5 AND temp > 15°C | Critical | Increase acaricide spraying to every 5–7 days during extended wet, warm period; inspect all animals daily for tick attachment; check for tick-borne disease signs: lethargy, high fever, reduced milk, swollen lymph nodes; remove stagnant water—empty tyres, buckets; apply pyrethroid pour-on if fly burden visible |
| VEC-003 | Peak tick emergence after heavy rain — 72h rain > 30 mm, temp 20–30°C | 72h rain > 30 mm AND temp 20–30°C | Critical | Spray all cattle with acaricide today—this is the most critical prophylactic window; inspect all animals for tick attachment; alert neighbouring farmers for coordinated treatment; watch for ECF signs 2–3 weeks from now; contact vet for emergency ITM vaccination if not done this season |
| VEC-004 | Long rains tick season — March–May, temperature 18–28°C | Month in [3,4,5] AND temp 18–28°C | High | Increase acaricide spraying to at least every 7 days during March–May; check all animals daily for tick attachment—pay special attention to ears & udder; ensure ECF vaccination is current; record milk yield daily—unexplained drop is early sign of tick-borne disease; stock treatment drugs: oxytetracycline & buparvaquone (Butalex) |
| VEC-005 | Short rains tick season — October–November, temperature 18–28°C | Month in [10,11] AND temp 18–28°C | High | Resume weekly acaricide spraying from October 1; check animals daily for tick attachment; review acaricide records—rotate to different class if same product used all year; stock treatment drugs; inspect animals for condition score—poor condition = more susceptible |
| VEC-006 | Post-drought first rain — tick questing surge (dry > 336 hours, rain today > 5 mm) | Hours since last rain > 336 AND rain today > 5 mm | High | Apply acaricide spray within 24 hours of first significant rain after dry spell; inspect all animals for already-attached ticks; alert herd owner—tick-borne disease risk elevated for next 3–4 weeks; do not move cattle to new paddocks immediately after first rain—reinfestation risk |
| VEC-007 | Fly & tick vector season — warm, humid, rainy months (temp 15–30°C, RH > 70%, months 3,4,5,10,11) | Temp 15–30°C AND RH > 70% AND month in [3,4,5,10,11] | Medium | Inspect all animals for tick load at least every 3 days; apply acaricide on regular schedule—at minimum every 10 days; remove stagnant water—essential for fly control; apply pyrethroid pour-on if fly annoyance causing production loss; record any unexplained fever or milk drop |
| VEC-008 | Heavy cumulative rainfall — broad tick & vector alert (7-day rain > 50 mm) | 7-day cumulative rain > 50 mm | Medium | Maintain weekly acaricide spraying—do not reduce frequency even if individual tick burden looks low; pastures will remain tick-infested for 3–4 weeks minimum; inspect all animals twice weekly for tick attachment; check for signs of tick-borne disease: fever, milk drop, swollen lymph nodes |

---

## PARASITES (4 rules)

| ID | Name | Trigger Condition | Priority | Key Actions |
|---|---|---|---|---|
| PARA-001 | Internal parasite (worm) risk — extended dry spell (dry > 30 days) | Consecutive dry days > 30 | High | Conduct strategic deworming at end of dry spell—before rains arrive; weigh all animals & dose by bodyweight—never by estimate; perform faecal egg count (FEC) if possible; move animals away from heavily grazed water-point areas; check body condition score—weight loss may indicate high worm burden |
| PARA-002 | Worm development conditions — rain & warmth (72h rain > 15 mm, temp > 18°C) | 72h rain > 15 mm AND temp > 18°C | Medium | Assess need for deworming in 3–4 weeks by monitoring FEC or body condition; rotate pastures now to allow rest—larvae on resting paddocks die over 4–6 weeks; check calves & young stock closely—most susceptible; look for signs of worm burden 2–3 weeks: diarrhoea, bottle jaw, weight loss, poor coat |
| PARA-003 | Strategic deworming month — May or November | Month in [5,11] | Medium | Conduct strategic deworming this month—end of rainy season is optimal treatment window; use FEC to select which animals to treat—do not blanket-treat unless warranted; weigh all cattle & dose accurately—under-dosing promotes anthelmintic resistance; rotate to different anthelmintic class; include liver fluke treatment if farm has wet, low-lying areas |
| PARA-004 | Liver fluke (Fasciola) risk — extended wet period (wet > 7 days, temp 18–28°C) | Consecutive wet days > 7 AND temp 18–28°C | Medium | Restrict access to wet, low-lying paddocks & water bodies where snails breed; check for liver fluke signs 6–8 weeks from now: bottle jaw, poor condition, reduced milk yield; include liver fluke treatment (triclabendazole) in next deworming round; drain any permanently wet areas in paddocks if possible |

---

## NUTRITION_FORAGE (6 rules)

| ID | Name | Trigger Condition | Priority | Key Actions |
|---|---|---|---|---|
| NUTR-001 | Forage scarcity — dry spell > 21 days | Consecutive dry days > 21 | High | Increase dairy meal supplementation: calculate (milk kg − 5) ÷ 2 = kg meal/day; begin drawing on silage/hay reserves—do not wait until exhausted; assess remaining forage supply: count days of reserve at current consumption; reduce grazing in heavily depleted paddocks; provide mineral lick or loose mineral supplement |
| NUTR-002 | Severe forage shortage — dry spell > 42 days | Consecutive dry days > 42 | Critical | Calculate feed budget: litres milk/day × 0.45 = minimum kg meal needed; begin rationing silage/hay—if reserves critically low, source emergency forage now; reduce stocking rate if necessary; provide protein supplement (sunflower cake, cotton seed cake); check BCS on all cows—do not allow below 2.5; ensure water availability—dehydration worsens stress |
| NUTR-003 | Nutritional support during heat stress — THI > 72 | THI > 72 | Medium | Increase energy density of ration—add bypass fat or concentrate if available; feed during cooler hours (early morning & evening); ensure access to clean, cool water at all times; adjust dairy meal: (milk kg − 5) ÷ 2 = kg meal/day; provide electrolyte supplement if cows panting heavily |
| NUTR-004 | Early dry season nutrition alert — dry > 14 days | Consecutive dry days > 14 | Medium | Begin supplementary feeding—add 1–2 kg dairy meal/cow/day above maintenance; assess silage & hay stocks—project consumption for remaining dry season; implement rotational grazing—rest each paddock ≥3 weeks; check water quality—dry season can concentrate minerals in bore water |
| NUTR-005 | First rain after dry spell — grazing management (rain > 10 mm after dry > 14 days) | Rain today > 10 mm AND consecutive dry days > 14 | Medium | Hold cattle off freshly rained paddocks for ≥7 days to allow grass to reach 15+ cm; continue supplementary feeding until new pasture adequate height; watch for bloat when cattle first turned onto lush pasture; graze rested paddocks first—highest quality regrowth; consider topping overgrown paddocks before regrazing |
| NUTR-006 | Cold weather nutrition — increased energy needs (min < 12°C) | Min temp < 12°C | Medium | Increase dairy meal ration by 0.5–1 kg/cow/day during cold nights; ensure ad-libitum access to high-quality roughage—hay/silage at night; check water trough temperature—cattle drink less from very cold water; watch for weight loss in calves—highest cold-related energy demand |

---

## WATER (4 rules)

| ID | Name | Trigger Condition | Priority | Key Actions |
|---|---|---|---|---|
| WATR-001 | Increased water demand — heat stress (THI ≥ 72) | THI ≥ 72 | High | Increase water supply by ≥30 L/cow/day above baseline (total 90–120 L/cow/day); check all troughs full & automatic refill working; provide water near feed—cows drink mainly within 30 min of eating; ensure water temp below 20°C—warm water reduces intake; check for competition at troughs—dominant cows can restrict others |
| WATR-002 | Critical water demand — severe heat stress (THI ≥ 78) | THI ≥ 78 | Critical | Ensure 100+ L/cow/day water available at all times; change water in troughs twice daily to maintain cool temp (< 20°C); provide multiple water access points—dominant cows block subordinates at single troughs; use water to wet/cool cows directly—wetting reduces rectal temp faster than drinking; monitor for dehydration: dry muzzle, skin tenting, sunken eyes—call vet if present |
| WATR-003 | High water demand — hot day (max > 32°C) | Max temp > 32°C | High | Check all water troughs this morning—ensure full before peak heat (11 am–3 pm); provide shade near troughs—cows stand near water in hot conditions; move milking to cooler hours if water limited; top up trough supply in afternoon if automatic refill unavailable |
| WATR-004 | Water supply risk — extended dry spell (dry > 21 days) | Consecutive dry days > 21 | High | Assess current water source levels—check stream flow, bore yield, tank storage; identify backup water sources in case primary fails; reduce non-essential water uses (washing) to prioritise cattle drinking water; check water quality in remaining surface sources—algae & bacteria concentrate as levels fall; contact water vendor or plan emergency supply now if primary at risk |

---

## REPRODUCTION (4 rules)

| ID | Name | Trigger Condition | Priority | Key Actions |
|---|---|---|---|---|
| REPR-001 | AI conception risk — severe heat stress in breeding season (THI ≥ 78, June–August) | THI ≥ 78 AND month in [6,7,8] | Critical | Delay AI until September when temperatures moderate—conception rate recovers quickly; if AI cannot be delayed, perform at earliest morning opportunity (4–5 am) when THI at daily minimum; provide shade & cool water 48 hours before & after AI; detect heat 3 times daily (morning, noon, evening)—heat expression reduced in stressed cows; consider progesterone CIDR synchronisation |
| REPR-002 | Newborn calf hypothermia risk — cold nights in calving season (min < 10°C, Feb–March) | Min temp < 10°C AND month in [2,3] | Critical | Check all heavily pregnant cows at night—calves born in cold need immediate attention; dry newborn calves with towel immediately; bring newborns indoors/into sheltered, bedded pen immediately; feed 2 L colostrum within 30 minutes of birth; check rectal temperature of newborn: < 37°C requires emergency warming (warm water bath or heat lamp); monitor dam closely for retained placenta or metritis |
| REPR-003 | Calving emergency — cold wet conditions at calving (rain > 5 mm, min < 14°C, Feb–March) | Rain today > 5 mm AND min temp < 14°C AND month in [2,3] | Critical | Move all heavily pregnant cows into calving pen NOW; check for calving cows every 2 hours day & night; dry calf immediately with towel—move into warm, dry pen; feed 2 L colostrum within 30 minutes—do not wait for calf to stand; tube-feed colostrum using oesophageal feeder if calf cannot suckle; watch dam for milk fever, retained placenta, or prolapse |
| REPR-004 | Heat stress reduces AI success — THI ≥ 72 in breeding season (June–August) | THI ≥ 72 AND month in [6,7,8] | High | Detect heat at minimum 3 times daily (5 am, midday, 6 pm); perform AI in early morning when cow temp lowest—before 8 am; ensure shade & cool water 48 hours before & after AI; record conception results carefully—if < 50%, consider waiting for cooler months; use tail paint or activity monitors to improve heat detection accuracy |

---

## SPRAYING (3 rules)

| ID | Name | Trigger Condition | Priority | Key Actions |
|---|---|---|---|---|
| SPRY-001 | Acaricide spraying blocked — rain expected (rain probability next 6h > 40%) | Rain probability next 6h > 40% | High | Do not apply acaricide today if rain probability > 40% in next 6 hours—rain washes product off before absorption; reschedule spraying to next dry morning—ideally before 9 am; if tick burden critical & cannot wait, apply in evening window after rain risk passes; check 24-hour forecast for best dry window in next 2 days |
| SPRY-002 | Acaricide spraying blocked — high wind (wind > 15 km/h) | Wind speed > 15 km/h | High | Do not spray acaricide when wind > 15 km/h—causes spray drift, uneven coverage, missed sites, & operator inhalation; delay until wind calms; best spray window is early morning (6–9 am) when wind typically lightest; use pour-on acaricide applied to backline if urgent—less drift-sensitive; stand upwind of animal when spraying |
| SPRY-003 | Acaricide spraying blocked — rainfall today (rain > 2 mm) | Rain today > 2 mm | High | Do not spray acaricide today—product washed off by rain, leaving animals unprotected while ticks most active; reschedule for next dry morning with < 2 mm rain forecast; if tick burden severe & cannot wait, use pour-on acaricide under cover—less rain-sensitive; hand-remove engorged ticks from sensitive areas as emergency measure |

---

## Notes & Reference

### THI (Temperature-Humidity Index) Formula

The THI value used throughout these rules is calculated as:

```
THI = 0.8 × T + (RH/100) × (T − 14.4) + 46.4
```

Where:
- **T** = Temperature in degrees Celsius
- **RH** = Relative humidity as a percentage (0–100)

### THI Thresholds

| THI Range | Interpretation | Dairy Cow Status |
|---|---|---|
| < 72 | Comfortable | No heat stress; normal feeding & production |
| 72–77 | Mild stress | Increased water intake; mild milk production loss (5–10%) |
| ≥ 78 | Severe stress | Emergency cooling needed; milk loss 15–25%; conception rates fall 20–30% |

### Weather Fields Reference

The rules monitor these key weather and derived fields:

| Field | Definition | Units |
|---|---|---|
| `thi_value` | Temperature-Humidity Index (calculated daily) | Index (unitless) |
| `temperature_max_c` | Daily maximum temperature | °C |
| `temperature_min_c` | Daily minimum temperature | °C |
| `temperature_c` | Current/mean temperature | °C |
| `relative_humidity_pct` | Relative humidity | % (0–100) |
| `qpf_today_mm` | Quantitative precipitation forecast for today | mm |
| `cumulative_rain_72h_mm` | Rain over past 72 hours | mm |
| `cumulative_rain_7d_mm` | Rain over past 7 days | mm |
| `consecutive_dry_days` | Number of consecutive days without rain (> 0.5 mm) | days |
| `consecutive_wet_days` | Number of consecutive days with measurable rain | days |
| `wind_speed_kmh` | Wind speed | km/h |
| `temperature_change_24h_c` | Change in temperature over past 24 hours | °C |
| `temperature_trend` | Direction of temperature change | "rising", "falling", "stable" |
| `hours_since_last_rain` | Hours elapsed since last measurable rainfall | hours |
| `rain_probability_next_6h_pct` | Probability of rain in next 6 hours | % (0–100) |
| `month` | Current month (1–12) | integer |

### How to Read These Rules

1. **When a rule triggers:** Weather conditions match the "Trigger Condition" column. The system generates an advisory with this rule's name, priority, and key actions.

2. **Priority levels guide urgency:** Critical rules require immediate action within hours. High priority rules need attention within 24–48 hours. Medium and informational rules are for monitoring and planning.

3. **Actions are specific and sequenced:** Each rule lists concrete steps in order of importance. Follow the sequence and do not skip steps (especially teat dipping in mastitis protocols, shade provision in heat stress, and vaccination in respiratory disease).

4. **Preventive actions reduce future risk:** These are listed separately because they require advance planning (e.g., building silage reserves before dry season, installing shade structures before hot season, vaccinating calves before cold season).

5. **Rules apply to "all" stages by default:** Unless a rule specifies otherwise (e.g., "calving season only"), it applies to all herd stages. Some rules specify "drying off" or "peak lactation" to narrow context.

6. **Spraying rules are practical constraints:** Rules in the "SPRAYING" category block acaricide (tick spray) application when weather makes it ineffective—rain washes it off, wind causes drift. Always check these rules before scheduling spray days.

7. **Water and nutrition rules compound heat & cold stress:** Heat stress increases water demand by 30+ L/day. Cold stress increases energy (meal) demand. Combining heat with dry forage, or cold with inadequate shelter, creates emergency situations—prioritise multiple actions at once.

8. **Vector (tick) rules have seasonal patterns:** March–May and October–November are peak tick seasons in Kenya. October–November is especially dangerous because tick-borne disease vaccines may have waned since long rains. Review acaricide rotation before short rains begin.

9. **Reproductive rules centre on avoiding heat stress timing:** June–August heat stress reduces conception rates by 20–30%. Planning AI to October–November (cooler months) dramatically improves herd calving patterns and reduces off-season production.

10. **Mastitis prevention is year-round:** Teat pre-dip and post-dip are critical every single day, especially during rainy seasons. Dry cow therapy (DCT) at dry-off in wet months is mandatory. Subclinical mastitis (detected by CMT, not visible) damages next lactation—it is not a minor issue.

### Practical Integration

- **Daily check:** Before morning milking, consult today's weather. If any heat stress rule triggers, plan shade/water/feeding timing adjustments for the day.
- **Weekly check:** Review moisture, water source, and forage supply status. If consecutive dry days approaching 14+, start drawing down stored feeds and supplementing.
- **Seasonal check (monthly):** At the start of each month, align the herd with seasonal disease/pest pressure. March–April is high anthracnose season in avocado, but for dairy it is peak tick & mastitis season—check tick acaricide stock and mastitis protocols.
- **Vector management (ongoing):** Coordinate spraying with neighbouring farms if possible. Individual farms spraying while neighbours do not creates reinfection pressure. Rotate acaricide classes every 3 months to prevent resistance.

---

**Document version 1.0 | Generated 30 April 2026**

For questions or updates, contact the advisory system administrator or the source organisations listed above.
