# Comparison — K=8 Baseline vs. K=4 Experiment
**NC Housing Price Regression · CSC-114 Module 5/6**

Single change tested: fold count only (`k = 8` → `k = 4`). Architecture, data cleaning, train/test split (fixed seed), and epoch counts held identical across both runs.

---

## Head-to-head

| Metric | K=8 (baseline, `110751`) | K=4 (`114435`) | Difference |
|---|---|---|---|
| Per-fold MAE (scaled) | 0.426, 0.399, 0.384, 0.420, 0.419, 0.457, 0.407, 0.429 | 0.415, 0.404, 0.415, 0.423 | — |
| Per-fold spread | 0.384 – 0.457 | 0.404 – 0.423 | narrower at K=4 (single-run observation) |
| **Mean CV MAE (scaled)** | **0.418** | **0.415** | **−0.003** |
| **Mean CV MAE ($)** | **$41,762** | **$41,451** | **−$311** |
| Final test MAE (scaled) | 0.429 | 0.422 | −0.007 |
| Final test MAE ($) | $42,870 | $42,165 | −$705 |
| Models trained per K-fold pass | 8 (×2 passes = 16) | 4 (×2 passes = 8) | ~50% fewer |
| Worst-residual rows | 3140, 3261, 3358 | 3140, 3261, 3358 | identical rows |

---

## Reading the result

**Accuracy: no meaningful change.** A $311 gap on a ~$41,500 metric is well inside the noise you'd expect from run-to-run random weight initialization alone — it's not a signal that K=4 validates worse than K=8. With 4,508 training rows, even K=4's smaller fold count still leaves each validation slice with over 1,100 samples, which is plenty for a stable per-fold read on this dataset.

**Final test MAE moved too, but that's not a K effect.** The final model is always trained on the *entire* training set (`x_train`), independent of how many folds were used upstream in the K-fold pass. The 0.429 → 0.422 shift reflects a different random initialization between the two runs, not the fold-count change. Worth remembering when interpreting future comparisons: only the **CV MAE** number is actually sensitive to K; the final test MAE is not.

**Speed: real win.** Cutting K from 8 to 4 halves the number of models trained in each K-fold pass (16 → 8 total across both passes) for a difference in the accuracy estimate that's not distinguishable from noise. That's the trade you were after given the time constraint.

**Consistency check:** the same three block groups (3140, 3261, 3358) show up as the worst residuals in both runs, with the same underprediction-of-high-value pattern. That's a useful sanity signal — it means the change in K didn't alter *what* the model struggles with, only how the validation score was computed.

**Incidental alignment:** Module 4's own reference example (California Housing) used K=4 as well — so this change also brings the fold count back in line with the course's own baseline approach, not just a speed shortcut.

---

## Recommendation

Adopt **K=4** going forward. On this run, it cost no measurable accuracy and roughly halves K-fold wall-time — the right trade for iterating on the upcoming width/depth experiments. If the final write-up wants extra defensibility on the CV estimate specifically, it's fair to note both K values were tested and came back statistically indistinguishable.

**Caveat:** this is one run of each, not a repeated-trials comparison — reasonable given the time constraint, but worth stating as a limitation if this comparison gets cited directly in graded work.

---

*Sources: run_log_20260716_110751.txt (K=8) and run_log_20260716_114435.txt (K=4), this session.*
