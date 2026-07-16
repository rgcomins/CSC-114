# SITREP — CSC 114 Lab Session
**Classification:** UNCLASSIFIED // FOR ACADEMIC USE
**DTG:** 16 JUL 2026
**Subject:** MSE/RMSE Tracking — First Validation Run (Baseline Architecture)
**Prepared for:** Rick (CSC 114, Section 1001)

---

## BLUF
MSE/RMSE patch validated end-to-end: 6 plots generated (2 new MSE curves), all console output correct, no errors. Baseline architecture (2×64, K=4) results are consistent with the prior baseline run — confirms the new instrumentation didn't change training behavior. RMSE ($65K) meaningfully exceeds MAE ($42K) — a real, correctly-computed signal that error is tail-driven. Two claims from the initial pass at this run needed correction before write-up use (see below).

---

## SITUATION
First run using the patched script (MSE/RMSE capture in K-fold pass 1, per-epoch MSE curve in pass 2, test-set MSE/RMSE). Architecture and fold count unchanged from the standing baseline (`Dense(64)×2`, K=4) — this run's purpose was to validate the new instrumentation, not to test a new architecture.

---

## TASKS COMPLETED

| # | Task | Outcome |
|---|---|---|
| 1 | Run patched script, confirm no errors | Complete — all 6 plots + log saved, stamp `20260716_123043` |
| 2 | Confirm MAE results match prior baseline (parity check) | Complete — CV MAE $41,375 vs. prior $41,451; test MAE $42,123 vs. prior $42,165 |
| 3 | Verify MSE/RMSE arithmetic in the run log | Complete — every printed value checks out |
| 4 | Ground the "Claude Code" interpretive claims against the data | Complete — 2 of 4 claims needed correction (see below) |
| 5 | Compare MSE curve shape vs. MAE curve shape, this run | Complete — no meaningful difference; both are noisy plateaus |

---

## RUN RESULTS (Dense(64)×2, K=4, 50 epochs, full — not quick)

| Metric | Cross-val (K=4) | Held-out test |
|---|---|---|
| MAE (scaled) | 0.414 → $41,375 | 0.421 → $42,123 |
| MSE (scaled) | 0.422 | 0.430 |
| RMSE (scaled) | 0.650 → $64,988 | 0.656 → $65,576 |
| RMSE − MAE gap (scaled) | 0.236 | 0.235 |
| RMSE / MAE ratio | ~1.57× | ~1.56× |

Per-fold MAE: 0.419, 0.400, 0.421, 0.414
Per-fold MSE: 0.443, 0.342, 0.469, 0.435
Per-fold RMSE − MAE gap: 0.247, 0.185, 0.264, 0.246 — real spread, not tightly clustered around the mean.

---

## CORRECTIONS TO THE INITIAL PASS

1. **"None of the three architecture experiments closed the RMSE−MAE gap"** — unsupported. MSE/RMSE tracking didn't exist when the width and depth experiments ran; those runs only ever recorded MAE. There is no RMSE data for 2×128 or 3×64. This is a real open question, not an answered one — see Next Actions.
2. **"The gap is stable... a real, reproducible property, not a fluke of one split"** — overstated based on aggregate-only comparison. Individual fold gaps range 0.185–0.264 (see table above), meaningful spread underneath the two close-together averages. The gap's *existence and rough size* holds up across CV and test; fold-to-fold stability is not demonstrated.

What does hold up: the RMSE/MAE ratio (~1.56–1.57×) is a valid, correctly-computed indicator of tail-driven error, and it ties cleanly to the same three block groups (3261, 3140, 3358) that have appeared as the worst residuals in every run so far, regardless of architecture, fold count, or this run's new instrumentation.

---

## CURRENT STATUS

- Model: `Dense(64) → Dense(64) → Dense(1)` (baseline) — confirmed unchanged behavior with MSE/RMSE instrumentation added
- K-fold: K=4 — CV MAE $41,375, CV RMSE $64,988
- Final model: Test MAE $42,123, Test RMSE $65,576
- Worst residuals: same 3 block groups as every prior run — consistency holds across every configuration tested to date

---

## NEXT ACTIONS

| Priority | Action |
|---|---|
| HIGH | If the width-vs-depth-vs-RMSE question matters for the write-up, re-run the 2×128 and/or 3×64 configurations with the now-patched script to get real RMSE data for them — currently untested |
| LOW | Merge quick-mode epoch count fix (10→30) into the working copy |

---

*Source: run_log_20260716_123043.txt and accompanying plots, this session.*
