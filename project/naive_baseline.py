"""
Standalone naive (predict-the-mean) baseline for the NC Housing regression.

Mirrors the loading, cleaning, split, and target-scaling of nc_housing_model_v1.py
exactly (same seed, same k) so the baseline MAE is directly comparable to the
model's k-fold validation MAE and test MAE. Does NOT touch the model script.

Run: python naive_baseline.py --data NC_Housing_Prices_ready.csv
"""

import argparse
import numpy as np

from nc_housing_model_v1 import load_and_clean, TARGET_COL, TARGET_SCALE


def main(data_path):
    df = load_and_clean(data_path)
    feature_cols = [c for c in df.columns if c != TARGET_COL]
    data = df[feature_cols].to_numpy(dtype="float32")
    targets = df[TARGET_COL].to_numpy(dtype="float32")

    # Same 80/20 split as the model
    rng = np.random.default_rng(seed=42)
    indices = rng.permutation(len(data))
    split = int(len(data) * 0.8)
    train_idx, test_idx = indices[:split], indices[split:]
    train_targets, test_targets = targets[train_idx], targets[test_idx]

    y_train = train_targets / TARGET_SCALE
    y_test = test_targets / TARGET_SCALE

    # ---- Naive baseline on the held-out test set ----
    baseline_pred = y_train.mean()
    test_baseline_mae = np.mean(np.abs(y_test - baseline_pred))
    print(f"Naive baseline (predict train mean) on TEST set:")
    print(f"  MAE (scaled): {test_baseline_mae:.3f}  ->  ${test_baseline_mae * TARGET_SCALE:,.0f}")

    # ---- Naive baseline across the same k-fold validation splits ----
    k = 8
    num_val_samples = len(y_train) // k
    fold_baseline_maes = []
    for i in range(k):
        fold_y_val = y_train[i * num_val_samples : (i + 1) * num_val_samples]
        fold_y_train = np.concatenate(
            [y_train[: i * num_val_samples], y_train[(i + 1) * num_val_samples :]],
            axis=0,
        )
        pred = fold_y_train.mean()
        fold_baseline_maes.append(np.mean(np.abs(fold_y_val - pred)))
    mean_fold_baseline = float(np.mean(fold_baseline_maes))
    print(f"Naive baseline across k={k} validation folds:")
    print(f"  Mean MAE (scaled): {mean_fold_baseline:.3f}  ->  ${mean_fold_baseline * TARGET_SCALE:,.0f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="NC_Housing_Prices_ready.csv")
    args = parser.parse_args()
    main(args.data)
