# SITREP — CSC 114 Lab Session
**Classification:** UNCLASSIFIED // FOR ACADEMIC USE
**DTG:** 16 JUL 2026
**Subject:** Depth Experiment — Dense(64)×3, K=4
**Prepared for:** Rick (CSC 114, Section 1001)

---

## BLUF
Third hidden layer added (`Dense(64)` ×3, same K=4 fold count and everything else held fixed). Run executed cleanly. This is the **worst-performing of the three architectures tested** — CV MAE $42,991 (vs. $41,451 baseline, +$1,540) and test MAE $42,999 (vs. $42,165 baseline, +$834). Neither width nor depth improved on the baseline; depth cost more than width did.

---

## SITUATION
Third "one change" experiment on the NC Housing model. Only a third `Dense(64, activation="relu")` layer added; K=4, data cleaning, train/test split, and epoch count held identical to the prior baseline and width-experiment runs.

---

## TASKS COMPLETED

| # | Task | Outcome |
|---|---|---|
| 1 | Add third Dense(64) layer, re-run | Complete — no errors, timestamp `20260716_120939` |
| 2 | Compare CV MAE and test MAE against baseline and width experiment | Complete — see three-way comparison doc |
| 3 | Verify per-fold spread against baseline range | Complete — minimum shifted up (0.404→0.417), 2 of 4 folds still fall within baseline's historical range |
| 4 | Check worst-residual rows across all three runs | Complete — mixed picture, corrected in comparison doc (see note below) |

---

## RUN RESULTS (Dense(64)×3, K=4, 50 epochs, full — not quick)

- Rows after cleaning: 5,635 (train 4,508 / test 1,127) — unchanged
- Per-fold MAE (scaled): 0.421, 0.417, 0.434, 0.448
- **Mean CV MAE: 0.430 → $42,991 off, on average**
- **Final test MAE: 0.430 → $42,999 off, on average**

---

## OBSERVATIONS

- **CV MAE rose more here than in the width experiment** (+$1,540 vs. baseline, compared to +$335 for width) — the larger of the two shifts seen so far, though still a single run.
- **Validation curve:** minimum lands earlier than the width run's (~epoch 12–15 here, ~epoch 12–15 range vs. ~18–20 for width), reaching a similar floor (~0.409–0.410) before rising with more noise, including a sharp spike near epoch 25 (~0.450) — noisier than the width run's curve but consistent with the same general post-minimum upward drift.
- **Residual tail — correction from the initial pass:** the earlier claim that the $1.04M block group (row 3358) declined smoothly across all three runs ($450K → $400K → $393K) doesn't hold up — the width-experiment prediction for that row was $449,967, essentially flat versus baseline, not ~$400K. The row that *does* show a clean, monotonic decline across all three architectures is the $608K block group (row 3140): $127,023 → $121,391 → $112,755. The $1.45M row (3261) doesn't fit a "worse with capacity" story at all — width actually improved its prediction before depth partially reversed that. Full numbers in the comparison doc.

---

## CURRENT STATUS

- Model tested this run: `Dense(64) → Dense(64) → Dense(64) → Dense(1)`
- Standing best-performing architecture remains the original baseline: `Dense(64) → Dense(64) → Dense(1)`
- K-fold: K=4, 50 epochs/fold — CV MAE 0.430 (~$42,991)
- Final model: 50 epochs — Test MAE 0.430 (~$42,999)

---

## NEXT ACTIONS

| Priority | Action |
|---|---|
| HIGH | Decide whether to formally close the architecture-experiment thread and revert to `Dense(64)×2` as the model going into the final write-up |
| MEDIUM | If citing a single-row example of capacity hurting tail predictions, use row 3140 ($608K), not row 3358 — it's the one that actually declines monotonically |
| LOW | Merge quick-mode epoch count fix (10→30) into the working copy |

---

*Source: run_log_20260716_120939.txt and accompanying plots, this session.*
