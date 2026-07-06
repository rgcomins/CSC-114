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

## What we are NOT doing (scope guard)
- Not building a general ACS-data cleaning pipeline — only repairing/dropping
  the known bad rows in this specific file (duplicated total_rooms /
  total_bedrooms, the 9999 sentinel, the bad housing_median_age row)
- Not re-deriving features from the raw Census API — using the pre-built CSV
- Not doing deployment or a UI — model + evaluation only

## Team & roles
Solo. Self-review, documented in the PR.
