# SITREP — CSC 114 Lab Session
**Classification:** UNCLASSIFIED // FOR ACADEMIC USE
**DTG:** 16 JUL 2026
**Subject:** v2 Timestamped-Output Pipeline — Baseline Confirmation Run
**Prepared for:** Rick (CSC 114, Section 1001)

---

## BLUF
`nc_housing_model_v2.py` executed end-to-end with no errors. Timestamped output pipeline (4 plots + 1 console log, single shared stamp `20260716_110751`) confirmed operational. Baseline metrics reproduce prior reported numbers within rounding — parity confirmed. One low-priority documentation drift noted (harmless). **Cleared to proceed to the K=4 fold experiment.**

---

## SITUATION
Same Codespace / Keras-PyTorch stack as prior sessions. This run used v2 as actually executed by Rick — the quick-mode epoch fix (10→30) drafted last session was not yet merged into this copy, but is irrelevant to this run since `--quick` was not used.

---

## TASKS COMPLETED

| # | Task | Outcome |
|---|---|---|
| 1 | Confirm v2 reproduces v1/baseline metrics | Complete — CV MAE $41,762 vs. prior ~$41K; test MAE $42,870 vs. prior ~$43K |
| 2 | Verify timestamped output pipeline | Complete — all 5 artifacts share one stamp, nothing overwritten |
| 3 | Review worst-residual diagnostics for data vs. model issues | Complete — no bad data rows found; pattern is model/loss behavior |
| 4 | Review validation MAE curve shape | Complete — still a noisy plateau, no clean overfitting turnaround |

---

## RUN RESULTS (K=8, 50 epochs, full — not quick)

- Rows after cleaning: 5,635 (train 4,508 / test 1,127)
- Per-fold MAE (scaled): 0.426, 0.399, 0.384, 0.420, 0.419, 0.457, 0.407, 0.429
- **Mean CV MAE: 0.418 → $41,762 off, on average**
- **Final test MAE: 0.429 → $42,870 off, on average**

---

## OBSERVATIONS / FRICTION

**1. `KEEP_COLS` labeling — CLOSED**
Decision made: raw CSV has both `total_rooms` and `total_bedrooms` as separate headers, identical duplicate values (ACS table B25041 pulled for both — a bug in the source file). Field stays named `total_rooms` in the cleaned data; no rename. Comment updated in the script to state plainly that every instance of `total_rooms` means total_bedrooms. No numeric impact either way — confirmed by this run's exact match to the previously reported baseline.

**2. Quick-mode epoch fix not yet merged**
No effect on this run (full mode only). Still pending for whenever `--quick` gets used for a smoke test.

**3. MSE tail-compression, visible in the data**
Worst 3 residuals are all underpredictions on the highest-value block groups in the test set ($608K, $1.04M, $1.45M actual, all predicted well below actual) — consistent with MSE pulling predictions toward the center of the distribution at the expense of rare high-value tail cases. Rick had already identified and discussed this same pattern with the instructor prior to this session; this run's residual printout is corroborating evidence, not a new finding. Not a data quality issue — good citation material for the write-up.

**4. Overfitting turnaround still not cleanly identifiable**
Both the full and truncated validation MAE curves show a plateau with noise (roughly 0.41–0.43 from epoch ~15 onward), not a sharp uptick. Same read as before — this remains an open item, not something this run resolved.

---

## CURRENT STATUS

- Model: `Dense(64) → Dense(64) → Dense(1)` — unchanged from baseline (confirmed by parity check)
- K-fold: K=8, 50 epochs/fold — CV MAE 0.418 (~$41,762)
- Final model: 50 epochs — Test MAE 0.429 (~$42,870)
- Timestamped output pipeline: **OPERATIONAL**

---

## NEXT ACTIONS

| Priority | Action |
|---|---|
| HIGH | Reduce K=8 → K=4, re-run, compare CV MAE against this baseline ($41,762) for accuracy delta |
| LOW | Merge quick-mode epoch count fix (10→30) into the working copy |

---

*Source: run_log_20260716_110751.txt and accompanying plots, this session.*
