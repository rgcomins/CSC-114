# SITREP — CSC 114 Module 5/6 Mini-Project
**Classification:** UNCLASSIFIED // FOR ACADEMIC USE
**DTG:** 15 JUL 2026
**Subject:** Model Re-run via Claude Code — Results Captured, One Config Flag
**Prepared for:** Rick (CSC 114, Section 1001)

---

## BLUF
Claude Code session (per handoff brief) re-ran the K=8 regression script end
to end. All 4 required plots generated, dollar-formatted predictions
produced, CV and test MAE captured. Source review of `nc_housing_model_v1.py`
resolved both open items from the prior SITREP: **the feature allowlist bug
is confirmed** — `total_rooms` (should be dropped) is kept, `total_bedrooms`
(should be kept) is never loaded — and **the housing_median_age zero-drop
result is expected**, not a bug (bad-age rows were already removed upstream,
per the script's own docstring). Neither blocks Check-In 1 (pipeline runs,
produces output), but the allowlist bug should be fixed before Check-In 2,
since results aren't trustworthy until it's training on the right column.

---

## TASKS COMPLETED

| # | Task | Outcome |
|---|---|---|
| 1 | Re-run K=8 regression script | Complete — ran clean end-to-end |
| 2 | Regenerate 4 required plots | Complete — all 4 saved |
| 3 | Capture CV + test MAE numbers | Complete |
| 4 | Before/after ablation on housing_median_age fix | Complete — separate plot, large improvement shown |
| 5 | Update `Sprint 1 Reflection.md` fact bullets with real numbers | Complete |
| 6 | Cross-check open questions against `nc_housing_model_v1.py` source | Complete — both resolved (see Incidents) |

---

## RESULTS CAPTURED

- Raw rows: 5,637 → 5,635 after cleaning (4,508 train / 1,127 test)
- Features used: `population, households, median_income, total_rooms,
  latitude, longitude, housing_median_age` (7 features)
- 8-fold CV mean MAE: 0.414 scaled → **~$41,407 off, on average**
  (per-fold: 0.387–0.435, tight spread)
- Final test MAE: 0.435 scaled → **~$43,466 off, on average**
- Worst 3 residuals: $-481,469 / $-493,870 / $-607,438 — two of the three
  involve high `median_income`, one at exactly $250,010 (likely an ACS
  top-code artifact, not a true value)
- Ablation (separate plot, `nc_housing_residuals_before_after.png`):
  removing bad-age rows took test MAE $54,370 → $44,522 and worst-case
  error $6.77M → $593,503

---

## INCIDENTS / FRICTION ENCOUNTERED

**Incident 1 — total_rooms/total_bedrooms allowlist mismatch — CONFIRMED, OPEN FIX**
Source review of `nc_housing_model_v1.py` confirms it: `KEEP_COLS` lists
`total_rooms`, not `total_bedrooms`. Since `total_rooms` is the documented
unrecoverable duplicate (wrong ACS table B25041 pulled for both columns), the
model is training on the wrong column. The script's own comment is stale/
backwards too — it references "total_rooms before it was dropped," which
doesn't match what the list actually does.
**Fix:** in `KEEP_COLS`, swap `"total_rooms"` → `"total_bedrooms"`; clean up
the misleading comment while there. `feature_cols` downstream derives itself
from `df.columns`, so no other code changes needed.

**Incident 2 — housing_median_age filter dropped 0 rows this run — RESOLVED**
Expected behavior, not a bug. The script's docstring names the expected
input as `NC_Housing_Prices_2018_age_cleaned.csv` — bad-age rows were already
stripped upstream, before this script runs. The in-script `!= 2018` filter
is a harmless no-op safety net on already-clean data.
**Minor note:** the `argparse` default path (`project/NC_Housing_Prices_ready.csv`)
doesn't match the docstring's stated filename — worth a quick alignment pass
so the two don't drift, but non-blocking.

---

## CURRENT STATUS

- Model: runs end-to-end, produces predictions + all 4 required plots ✅
- Check-In 1 bar ("is it alive"): **met** — pipeline takes data in, gives
  predictions out
- `Sprint 1 Reflection.md`: fact bullets updated with real numbers; the
  three graded answers are still TODO for Rick to write offline
- Naive baseline comparison: not yet computed (charter's "definition of good
  enough," not required for Check-In 1)
- Turnaround epoch: not yet read off the validation curve and named (same)

---

## NEXT ACTIONS

| Priority | Action |
|---|---|
| HIGH | Apply the one-line `KEEP_COLS` fix (`total_rooms` → `total_bedrooms`) and re-run |
| MEDIUM | Write the 3 graded reflection answers offline, in your own words |
| MEDIUM | Push branch, grab link, submit Check-In 1 |
| LOW | Align `argparse` default path with docstring's stated filename |
| LOW | Compute naive baseline + name turnaround epoch (needed before Check-In 2, not this one) |
| LOW | Run the awk trailing-comma root-cause diagnostic |

---

*Source: `output_07_15.txt` (Codespace run log) and
`nc_housing_residuals_before_after.png`, this session.*
