# SITREP — CSC 114 Lab Session
**Classification:** UNCLASSIFIED // FOR ACADEMIC USE
**DTG:** 16 JUL 2026
**Subject:** K=4 Fold Experiment — First "One Change" Test
**Prepared for:** Rick (CSC 114, Section 1001)

---

## BLUF
K reduced from 8 to 4 (single-line change, model architecture untouched). Run executed cleanly, no errors. Mean CV MAE $41,451 vs. baseline $41,762 at K=8 — a $311 difference, not meaningfully distinguishable from run-to-run noise. **K=4 does not cost measurable accuracy on this dataset and roughly halves K-fold wall-time. Cleared to adopt K=4 going forward.**

---

## SITUATION
First "one change" experiment on the NC Housing model, per the time-constraint call to test fold count before touching model shape. Only `k = 8` → `k = 4` changed; everything else (architecture, data cleaning, train/test split, epoch counts) held fixed.

---

## TASKS COMPLETED

| # | Task | Outcome |
|---|---|---|
| 1 | Change K=8 → K=4, re-run | Complete — no errors, timestamp `20260716_114435` |
| 2 | Compare CV MAE against K=8 baseline | Complete — see comparison doc |
| 3 | Check worst residuals for consistency with baseline | Complete — same 3 rows appear as worst in both runs |
| 4 | Review validation curve shape at K=4 | Complete — same noisy plateau pattern as K=8, no clean turnaround |

---

## RUN RESULTS (K=4, 50 epochs, full — not quick)

- Rows after cleaning: 5,635 (train 4,508 / test 1,127) — identical to baseline, data pipeline unaffected by K
- Per-fold MAE (scaled): 0.415, 0.404, 0.415, 0.423
- **Mean CV MAE: 0.415 → $41,451 off, on average**
- **Final test MAE: 0.422 → $42,165 off, on average**

---

## OBSERVATIONS

- Per-fold spread is tighter at K=4 (0.404–0.423) than K=8 (0.384–0.457), but this is a single run of each — not enough to conclude K=4 is inherently more stable without repeated trials. Worth treating as a data point, not a proven trend.
- Final test MAE differs slightly from baseline (0.422 vs. 0.429), but this isn't attributable to K — the final model always trains on the full training set regardless of fold count. The difference reflects random weight initialization between runs, not the fold change.
- Worst 3 residuals are the same rows as the K=8 run (block groups at index 3140, 3261, 3358) — same high-value underprediction pattern already discussed with the instructor, reconfirmed here.

---

## CURRENT STATUS

- Model: `Dense(64) → Dense(64) → Dense(1)` — still unchanged, no architecture experiment run yet
- K-fold: K=4, 50 epochs/fold — CV MAE 0.415 (~$41,451)
- Final model: 50 epochs — Test MAE 0.422 (~$42,165)

---

## NEXT ACTIONS

| Priority | Action |
|---|---|
| HIGH | Proceed to the width experiment (`Dense(64)` → `Dense(128)`, both hidden layers), using K=4 as the standing fold count |
| LOW | Merge quick-mode epoch count fix (10→30) into the working copy |

---

*Source: run_log_20260716_114435.txt and accompanying plots, this session.*
