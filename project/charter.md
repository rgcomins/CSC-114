# Project Charter: NC Housing Price Prediction

## What we're building (one sentence)
A regression model that predicts the median home value of a North Carolina
census block group from ACS features — same shape as the California Housing
model, reskinned onto NC's own dataset.

## Cohort
Tabular

## The data or tools we'll use
`NC_Housing_Prices_2018.csv` (D. Michael Senter, ACS 2018 5-year estimates +
TIGER/Line block-group centroids), loaded directly via `pandas.read_csv(url)`.
Same stack as Module 4: GitHub Codespaces, Keras 3 (PyTorch backend), Sacred
Flow branching/PR process.

## Definition of "good enough"
- Validation MAE beats the naive (predict-the-mean) baseline
- Validation MAE stops improving — name the turnaround epoch (same k-fold
  approach as Module 4)

### Results (measured 2026-07-15, k=8 folds, 50 epochs)
- **Naive (predict-the-mean) baseline:** ~$78,878 MAE (0.789 scaled),
  averaged across the same 8 validation folds; ~$77,808 on the held-out
  test set.
- **Model validation MAE:** **$41,407** (0.414 scaled), mean of the 8 folds
  — per-fold scaled MAE: [0.418, 0.425, 0.387, 0.411, 0.435, 0.415, 0.398,
  0.424]. Held-out **test MAE: $43,466** (0.435 scaled).
- **Criterion 1 — beats baseline:** ✅ met. $41,407 vs. $78,878 baseline —
  ~47% lower error than predicting the mean.
- **Criterion 2 — turnaround epoch:** validation MAE flattens around
  **epoch ~12–13**; after that it only oscillates in a noisy ~0.403–0.427
  band (global min near epoch 22, within noise), no sustained improvement.
- **Plots (saved under `project/`):**
  - Full validation MAE curve — `nc_housing_val_mae.png`
  - Truncated validation MAE curve (first 10 epochs dropped) —
    `nc_housing_val_mae_truncated.png`
  - Predicted vs. actual scatter — `nc_housing_pred_vs_actual.png`
  - Residual distribution — `nc_housing_residuals.png`
- Full run log: `project/output_07_15.txt`

## What we are NOT doing (scope guard)
- Not building a general ACS-data cleaning pipeline — only repairing/dropping
  the known bad rows in this specific file (duplicated total_rooms /
  total_bedrooms, the 9999 sentinel, the bad housing_median_age row)
- Not re-deriving features from the raw Census API — using the pre-built CSV
- Not doing deployment or a UI — model + evaluation only

## Team & roles
Solo. Self-review, documented in the PR.
