# SITREP — CSC 114 Lab Session
**Classification:** UNCLASSIFIED // FOR ACADEMIC USE
**DTG:** 16 JUL 2026
**Subject:** Width Experiment — Dense(64)→Dense(128), Both Hidden Layers
**Prepared for:** Rick (CSC 114, Section 1001)

---

## BLUF
Hidden layer width doubled (64→128 units, both layers), K=4 held fixed as the standing fold count, everything else unchanged. Run executed cleanly. Mean CV MAE essentially flat vs. the K=4 baseline ($41,786 vs. $41,451 — within noise), but final test MAE rose noticeably ($43,409 vs. $42,165), and the validation curve shows the clearest overfitting-style uptick seen yet in this project. **Net read: wider layers did not help, and show early signs of costing generalization on this dataset. Recommend not adopting width=128.**

---

## SITUATION
Second "one change" experiment on the NC Housing model. Only the two hidden `Dense` layers changed (64→128 units each); K=4, data cleaning, train/test split, and epoch count all held identical to the prior K=4 baseline run.

---

## TASKS COMPLETED

| # | Task | Outcome |
|---|---|---|
| 1 | Change Dense(64)×2 → Dense(128)×2, re-run | Complete — no errors, timestamp `20260716_115653` |
| 2 | Compare CV MAE and test MAE against K=4 baseline | Complete — see comparison doc |
| 3 | Check worst residuals for consistency | Complete — same 3 rows, mixed change in error magnitude |
| 4 | Review validation curve shape | Complete — first run showing a clear late-curve uptick |

---

## RUN RESULTS (Dense(128)×2, K=4, 50 epochs, full — not quick)

- Rows after cleaning: 5,635 (train 4,508 / test 1,127) — unchanged, data pipeline unaffected by model width
- Per-fold MAE (scaled): 0.412, 0.399, 0.446, 0.415
- **Mean CV MAE: 0.418 → $41,786 off, on average**
- **Final test MAE: 0.434 → $43,409 off, on average**

---

## OBSERVATIONS

- **CV MAE:** effectively unchanged from the K=4/width-64 baseline ($41,786 vs. $41,451, a $335 gap — not distinguishable from run-to-run noise).
- **Test MAE:** rose from $42,165 to $43,409 (+$1,244). One run each, so not conclusive on its own, but it lines up with the curve behavior below rather than contradicting it.
- **Validation curve — the notable finding this run:** earlier runs (both width-64, K=8 and K=4) showed a noisy but essentially flat plateau from roughly epoch 15 onward, with no clear rising trend. This run's curve dips to a minimum around **epoch ~18–20** (~0.409–0.410) and then trends upward with increasing noise through epoch 50, ending in a sharp spike (~0.4385) at the final epoch. This is the first run in the project showing a shape consistent with the classic overfitting signature — the widened model has enough extra capacity to start memorizing rather than just generalizing.
- **Worst residuals:** same three block groups as every prior run (3140, 3261, 3358) — the high-value-underprediction pattern persists regardless of width. Magnitudes shifted in both directions (one improved, two worsened slightly) — no clear systematic change to the tail-compression behavior from width alone.

---

## CURRENT STATUS

- Model: `Dense(128) → Dense(128) → Dense(1)` — this run only; prior baseline (`Dense(64)×2`) still the reference point
- K-fold: K=4, 50 epochs/fold — CV MAE 0.418 (~$41,786)
- Final model: 50 epochs — Test MAE 0.434 (~$43,409)

---

## NEXT ACTIONS

| Priority | Action |
|---|---|
| HIGH | Decide: revert to `Dense(64)×2` as the standing model, or run a second width value (e.g., 96) before concluding |
| MEDIUM | Consider using this run's curve (turnaround ~epoch 20) as a candidate answer for the long-open "name the turnaround epoch" item — first run with a clean-enough signal to point to |
| LOW | Merge quick-mode epoch count fix (10→30) into the working copy |

---

*Source: run_log_20260716_115653.txt and accompanying plots, this session.*
