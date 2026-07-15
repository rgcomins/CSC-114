# Sprint 1 Reflection — NC Housing Price Prediction

_Companion to `charter.md`. Cohort: Tabular. Sprint 1 re-run: 2026-07-15._

## Results (measured this sprint)

Re-ran the K=8 fold regression script (`project/nc_housing_model_v1.py`)
end-to-end on `NC_Housing_Prices_ready.csv`, 50 epochs per fold. Ran clean
from data-in to dollar-formatted predictions-out (exit 0). Full log:
`project/output_07_15.txt`.

| Metric | Scaled (÷100k) | Dollars |
| --- | --- | --- |
| Naive baseline (predict-the-mean), k-fold | 0.789 | ~$78,878 |
| Naive baseline (predict-the-mean), test set | 0.778 | ~$77,808 |
| **Model validation MAE (mean of 8 folds)** | **0.414** | **$41,407** |
| Model test MAE (held-out) | 0.435 | $43,466 |

- Per-fold validation MAE (scaled): [0.418, 0.425, 0.387, 0.411, 0.435,
  0.415, 0.398, 0.424].
- **Beats baseline:** yes — $41,407 vs. $78,878 is ~47% lower error than
  predicting the mean.
- **Turnaround epoch:** validation MAE flattens around **epoch ~12–13**.
  After that the average curve only oscillates in a noisy ~0.403–0.427 band
  (global minimum near epoch 22, within noise) — no sustained improvement.
- Naive baseline computed by a standalone helper (`project/naive_baseline.py`)
  that reuses the model script's exact load/clean/split/scaling, so the
  numbers are directly comparable.

### Saved plots (under `project/`)
- Full validation MAE curve — `project/nc_housing_val_mae.png`
- Truncated validation MAE curve (first 10 epochs dropped) —
  `project/nc_housing_val_mae_truncated.png`
- Predicted vs. actual scatter — `project/nc_housing_pred_vs_actual.png`
- Residual distribution — `project/nc_housing_residuals.png`

---

## Reflection questions (Rick — graded written responses)

> Drafted from my own session notes (`project/nc_housing_notes_v1.md`,
> `project/nc_housing_notes_v2.md`) plus this sprint's measured results.
> These are graded — review, edit, and make them my own before submitting.

### What actually runs?
The full regression script (`project/nc_housing_model_v1.py`) runs clean
end-to-end on `NC_Housing_Prices_ready.csv` — confirmed this sprint (exit 0),
from data-in to dollar-formatted predictions-out. It's the Chapter 4
California Housing example reskinned onto NC data: PyTorch backend (matches
the class stack), K=8 fold cross-validation (matches the Module 4
modification), dollar-formatted predictions, training-curve plots, plus the
new predicted-vs-actual scatter and residual histogram. The cleaning runs
too: the `usecols` allowlist keeps the phantom `Unnamed:` columns from ever
loading, the `9999` target sentinels are dropped, and the bad
`housing_median_age` rows are gone (the age-outlier rows were already removed
upstream in the "ready" file — the run confirms 5,635 rows survive cleaning).
End result: the model beats the naive baseline — $41,407 validation MAE vs.
~$78,878 for predict-the-mean (~47% lower error), and the validation curve
flattens around epoch ~12–13.

### What's broken?
Three known issues, none of them blocking Sprint 1:
- **`total_rooms` is unrecoverable, not repairable.** Both `total_rooms`
  and `total_bedrooms` were pulled from ACS table B25041 (bedrooms), so
  `total_rooms` never held real room counts — the correct fix is to drop it,
  not repair it, which is what we do.
- **Phantom trailing-column root cause is still unconfirmed.** The
  `usecols` allowlist is a solid workaround (and the script runs clean with
  it), but the underlying reason for the trailing commas in the raw CSV
  hasn't been formally confirmed — the `awk -F',' '{print NF}' | sort |
  uniq -c` field-count check hasn't been run yet.
- **The model struggles on high-end / unusual properties.** The worst
  residuals are legitimate expensive homes in the Charlotte area (actuals
  around $608K, $1.04M, and $1.45M, all badly under-predicted). We traced
  these back to the source spreadsheet and confirmed the numbers are real —
  so this is a model limitation on rare high-value blocks, not a data bug.
  Also inherent: the model predicts block-group (neighborhood) median value,
  not individual home price — the same granularity limit as California
  Housing.

### On track with scope?
Yes. Both of the charter's "good enough" criteria are met: validation MAE
beats the naive baseline ($41,407 vs. ~$78,878), and the turnaround epoch is
named (~12–13, where the curve flattens before oscillating in noise). We
stayed inside the scope guard — only the known bad rows were dropped/
repaired, we used the pre-built CSV rather than re-deriving from the Census
API, and there's no deployment or UI. What's deliberately left for later and
out of Sprint 1 scope: running the `awk` root-cause diagnostic (separate,
unblocked task), improving predictions on rare high-end properties, and
finalizing where the data-currency disclaimer lives.
