"""
before_after_residuals.py — Controlled before/after depiction of removing the
impossible housing_median_age == 2000 outlier rows.

Holds EVERYTHING constant (same source file, same feature columns, same split
seed, same normalization, same final-model architecture and epochs) and toggles
ONLY whether the two age==2000 rows are present. Produces a single side-by-side
residual-histogram figure so the effect is attributable to that one change.

Run: python before_after_residuals.py
"""

import os
os.environ.setdefault("KERAS_BACKEND", "torch")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import keras
from keras import layers

from nc_housing_model_v1 import KEEP_COLS, TARGET_COL, TARGET_SCALE

SOURCE = "not_cleaned/NC_Housing_Prices_2018.csv"
EPOCHS = 50

keras.utils.set_random_seed(42)  # reproducible weight init so the figure is stable


def base_clean(path):
    # Same load/clean as the model, EXCEPT we do not yet touch age==2000 —
    # that is the single variable we toggle below.
    df = pd.read_csv(path, usecols=KEEP_COLS)
    df = df[df[TARGET_COL].notna()]
    df = df[df[TARGET_COL] != 9999]
    df = df[df["housing_median_age"] != 2018]  # pre-existing cleaning
    df = df.dropna()
    return df.reset_index(drop=True)


def train_and_residuals(df, drop_age_2000):
    if drop_age_2000:
        df = df[df["housing_median_age"] != 2000].reset_index(drop=True)

    feature_cols = [c for c in df.columns if c != TARGET_COL]
    data = df[feature_cols].to_numpy(dtype="float32")
    targets = df[TARGET_COL].to_numpy(dtype="float32")

    rng = np.random.default_rng(seed=42)
    indices = rng.permutation(len(data))
    split = int(len(data) * 0.8)
    train_idx, test_idx = indices[:split], indices[split:]

    train_data, test_data = data[train_idx], data[test_idx]
    train_targets, test_targets = targets[train_idx], targets[test_idx]

    mean, std = train_data.mean(axis=0), train_data.std(axis=0)
    x_train = (train_data - mean) / std
    x_test = (test_data - mean) / std
    y_train = train_targets / TARGET_SCALE
    y_test = test_targets / TARGET_SCALE

    model = keras.Sequential([
        layers.Dense(64, activation="relu"),
        layers.Dense(64, activation="relu"),
        layers.Dense(1),
    ])
    model.compile(optimizer="adam", loss="mean_squared_error",
                  metrics=["mean_absolute_error"])
    model.fit(x_train, y_train, epochs=EPOCHS, batch_size=16, verbose=0)

    preds = model.predict(x_test, verbose=0).flatten() * TARGET_SCALE
    actual = y_test * TARGET_SCALE
    residuals = preds - actual
    mae = float(np.mean(np.abs(residuals)))
    return residuals, mae, len(df)


def main():
    df = base_clean(SOURCE)
    print(f"Rows after base clean (age==2000 still in): {len(df)}  "
          f"[age==2000 rows: {int((df['housing_median_age']==2000).sum())}]")

    res_before, mae_before, n_before = train_and_residuals(df, drop_age_2000=False)
    print(f"BEFORE (age==2000 kept):   n={n_before}  test MAE=${mae_before:,.0f}  "
          f"worst |error|=${np.max(np.abs(res_before)):,.0f}")

    res_after, mae_after, n_after = train_and_residuals(df, drop_age_2000=True)
    print(f"AFTER  (age==2000 removed): n={n_after}  test MAE=${mae_after:,.0f}  "
          f"worst |error|=${np.max(np.abs(res_after)):,.0f}")

    # ---- Side-by-side residual histograms ----
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    ax1.hist(res_before, bins=40, color="#c1666b")
    ax1.axvline(0, color="k", lw=0.8, ls="--")
    ax1.set_title(f"BEFORE — age≈2000 rows kept\ntest MAE \\${mae_before:,.0f}, "
                  f"worst error \\${np.max(np.abs(res_before)):,.0f}")
    ax1.set_xlabel("Prediction error (\\$)  [predicted − actual]")
    ax1.set_ylabel("Count")

    ax2.hist(res_after, bins=40, color="#4f9d69")
    ax2.axvline(0, color="k", lw=0.8, ls="--")
    ax2.set_title(f"AFTER — age≈2000 rows removed\ntest MAE \\${mae_after:,.0f}, "
                  f"worst error \\${np.max(np.abs(res_after)):,.0f}")
    ax2.set_xlabel("Prediction error (\\$)  [predicted − actual]")
    ax2.set_ylabel("Count")

    fig.suptitle("Residual distribution — before vs. after removing impossible-age rows",
                 fontsize=13)
    fig.tight_layout()
    out = "nc_housing_residuals_before_after.png"
    fig.savefig(out, dpi=120, bbox_inches="tight")
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
