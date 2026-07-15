"""
CSC-114 Module 5/6 — NC Housing Price Regression (Housing Reskin)
Adapted from Deep Learning with Python, 3rd Ed., Chapter 4, Example 3
(California Housing scalar regression), reskinned onto the NC Housing
dataset (D. Michael Senter, ACS 2018 5-year estimates).

Run:  python nc_housing_model_v1.py
Data: NC_Housing_Prices_ready.csv (the argparse default; or pass
      --data /path/to/file.csv)

By default plots are saved to PNG files so this runs headless in a
Codespace. Pass --show to open plot windows instead.

Note: the K-fold validation section trains many models and can take a
while. Use --quick to run fewer epochs for a fast smoke test.
"""

import argparse
import os

os.environ.setdefault("KERAS_BACKEND", "torch")  # matches your class stack; must be set before importing keras

import numpy as np
import pandas as pd
import matplotlib

import keras
from keras import layers


TARGET_COL = "median_house_value"
TARGET_SCALE = 100_000  # same convention as the CA Housing example — sanity-checked at runtime below

# Only these columns are trusted from the raw CSV. Phantom "Unnamed: N"
# columns from trailing commas in the source file are excluded here so they
# can't silently wipe the dataset via dropna() later.
#
# NOTE on total_rooms: in this dataset total_rooms and total_bedrooms were both
# pulled from ACS table B25041 (bedrooms) and are byte-for-byte identical, so
# the values stored under "total_rooms" are really bedroom counts (mislabeled
# in the source). The cleaned input (NC_Housing_Prices_ready.csv) ships only
# the "total_rooms" name, so that is what we allowlist. Renaming this entry to
# "total_bedrooms" would not change any prediction but would fail to load
# against that file, which has no such column.
KEEP_COLS = [
    "population",
    "households",
    "median_income",
    "median_house_value",
    "total_rooms",  # really B25041 bedroom counts — see NOTE above
    "latitude",
    "longitude",
    "housing_median_age",
]


def load_and_clean(path):
    # usecols restricts the read to exactly the trusted columns — phantom
    # "Unnamed: N" columns from trailing commas in the source file never get
    # loaded in the first place, so they can't silently wipe out dropna() later.
    df = pd.read_csv(path, usecols=KEEP_COLS)
    print("Raw rows:", len(df))
    print("Raw columns:", list(df.columns))

    # Drop rows where the target is missing or is the 9999 sentinel
    df = df[df[TARGET_COL].notna()]
    df = df[df[TARGET_COL] != 9999]
    print("After dropping missing/9999 target rows:", len(df))

    # Drop the bad housing_median_age == 2018 rows
    if "housing_median_age" in df.columns:
        df = df[df["housing_median_age"] != 2018]
    print("After dropping bad housing_median_age rows:", len(df))

    # Drop any remaining rows with missing values anywhere
    df = df.dropna()
    print("After dropping remaining NaNs:", len(df))

    return df


def get_model(input_dim):
    model = keras.Sequential(
        [
            layers.Dense(64, activation="relu"),
            layers.Dense(64, activation="relu"),
            layers.Dense(1),
        ]
    )
    model.compile(
        optimizer="adam",
        loss="mean_squared_error",
        metrics=["mean_absolute_error"],
    )
    return model


def main(data_path, show=False, quick=False, final_epochs=None):
    import matplotlib.pyplot as plt

    # ---- Load and clean the NC Housing dataset ----
    df = load_and_clean(data_path)

    feature_cols = [c for c in df.columns if c != TARGET_COL]
    print("Features used:", feature_cols)

    data = df[feature_cols].to_numpy(dtype="float32")
    targets = df[TARGET_COL].to_numpy(dtype="float32")

    print(f"Target range before scaling: ${targets.min():,.0f} - ${targets.max():,.0f}")
    if targets.max() < 1000:
        print("WARNING: target values look pre-scaled already — check TARGET_SCALE before trusting the dollar output below.")

    # ---- Train/test split (80/20, shuffled with a fixed seed for reproducibility) ----
    rng = np.random.default_rng(seed=42)
    indices = rng.permutation(len(data))
    split = int(len(data) * 0.8)
    train_idx, test_idx = indices[:split], indices[split:]

    train_data, test_data = data[train_idx], data[test_idx]
    train_targets, test_targets = targets[train_idx], targets[test_idx]

    print("Train data shape:", train_data.shape)
    print("Test data shape:", test_data.shape)

    # ---- Preparing the data: normalize features (train stats only), scale targets ----
    mean = train_data.mean(axis=0)
    std = train_data.std(axis=0)
    x_train = (train_data - mean) / std
    x_test = (test_data - mean) / std

    y_train = train_targets / TARGET_SCALE
    y_test = test_targets / TARGET_SCALE

    # ---- K-fold validation: estimate a single validation score ----
    k = 8
    num_val_samples = len(x_train) // k
    num_epochs = 10 if quick else 50
    all_scores = []
    for i in range(k):
        print(f"Processing fold #{i + 1}")
        fold_x_val = x_train[i * num_val_samples : (i + 1) * num_val_samples]
        fold_y_val = y_train[i * num_val_samples : (i + 1) * num_val_samples]
        fold_x_train = np.concatenate(
            [x_train[: i * num_val_samples], x_train[(i + 1) * num_val_samples :]],
            axis=0,
        )
        fold_y_train = np.concatenate(
            [y_train[: i * num_val_samples], y_train[(i + 1) * num_val_samples :]],
            axis=0,
        )
        model = get_model(x_train.shape[1])
        model.fit(
            fold_x_train,
            fold_y_train,
            epochs=num_epochs,
            batch_size=16,
            verbose=0,
        )
        _, val_mae = model.evaluate(fold_x_val, fold_y_val, verbose=0)
        all_scores.append(val_mae)

    print("Per-fold MAE (scaled):", [round(v, 3) for v in all_scores])
    mean_mae_scaled = float(np.mean(all_scores))
    print(f"Mean MAE (scaled): {mean_mae_scaled:.3f}  ->  ${mean_mae_scaled * TARGET_SCALE:,.0f} off, on average")

    # ---- K-fold validation: record the full MAE history per epoch ----
    num_epochs = 30 if quick else 50
    all_mae_histories = []
    for i in range(k):
        print(f"Processing fold #{i + 1}")
        fold_x_val = x_train[i * num_val_samples : (i + 1) * num_val_samples]
        fold_y_val = y_train[i * num_val_samples : (i + 1) * num_val_samples]
        fold_x_train = np.concatenate(
            [x_train[: i * num_val_samples], x_train[(i + 1) * num_val_samples :]],
            axis=0,
        )
        fold_y_train = np.concatenate(
            [y_train[: i * num_val_samples], y_train[(i + 1) * num_val_samples :]],
            axis=0,
        )
        model = get_model(x_train.shape[1])
        history = model.fit(
            fold_x_train,
            fold_y_train,
            validation_data=(fold_x_val, fold_y_val),
            epochs=num_epochs,
            batch_size=16,
            verbose=0,
        )
        all_mae_histories.append(history.history["val_mean_absolute_error"])

    average_mae_history = [
        np.mean([h[i] for h in all_mae_histories]) for i in range(num_epochs)
    ]

    # Plot the full validation MAE curve (scaled units, matching the book's convention)
    epochs = range(1, len(average_mae_history) + 1)
    plt.plot(epochs, average_mae_history)
    plt.xlabel("Epochs")
    plt.ylabel("Validation MAE (scaled)")
    plt.title("Average validation MAE per epoch — NC Housing")
    _output(plt, "nc_housing_val_mae.png", show)

    # Plot the same curve with the first 10 noisy epochs dropped — this is the one
    # to read yourself for the turnaround epoch; don't take the default on faith.
    plt.clf()
    truncated_mae_history = average_mae_history[10:]
    epochs = range(10, len(truncated_mae_history) + 10)
    plt.plot(epochs, truncated_mae_history)
    plt.xlabel("Epochs")
    plt.ylabel("Validation MAE (scaled)")
    plt.title("Average validation MAE (first 10 epochs dropped) — NC Housing")
    _output(plt, "nc_housing_val_mae_truncated.png", show)

    # ---- Train the final model and evaluate on the test set ----
    # Default final_epochs below is a placeholder — replace it with the epoch
    # where YOUR truncated curve above actually flattens (pass --final-epochs N).
    epochs_to_use = final_epochs or (30 if quick else 50)
    model = get_model(x_train.shape[1])
    model.fit(x_train, y_train, epochs=epochs_to_use, batch_size=16, verbose=0)
    test_mse, test_mae = model.evaluate(x_test, y_test)
    print(f"Test MAE (scaled): {test_mae:.3f}  ->  ${test_mae * TARGET_SCALE:,.0f} off, on average")

    # ---- Generating predictions on new data, converted back to dollars ----
    predictions_scaled = model.predict(x_test)
    predictions_dollars = predictions_scaled.flatten() * TARGET_SCALE
    actual_dollars = y_test * TARGET_SCALE

    print("\nFirst 5 test predictions vs. actual:")
    for pred, actual in zip(predictions_dollars[:5], actual_dollars[:5]):
        print(f"  Predicted: ${pred:,.0f}   Actual: ${actual:,.0f}   Error: ${pred - actual:,.0f}")

    # ---- Error graph 1: predicted vs. actual scatter ----
    plt.clf()
    plt.scatter(actual_dollars, predictions_dollars, alpha=0.4, s=15)
    lims = [
        min(actual_dollars.min(), predictions_dollars.min()),
        max(actual_dollars.max(), predictions_dollars.max()),
    ]
    plt.plot(lims, lims, "r--", label="Perfect prediction")
    plt.xlabel("Actual median house value ($)")
    plt.ylabel("Predicted median house value ($)")
    plt.title("Predicted vs. Actual — NC Housing test set")
    plt.legend()
    _output(plt, "nc_housing_pred_vs_actual.png", show)

    residuals = predictions_dollars - actual_dollars

    # ---- Diagnostic: inspect worst residuals (data vs. model check) ----
    worst_idx = np.argsort(np.abs(residuals))[-3:]
    print("\nWorst residuals — check these for data vs. model issues:")
    for idx in worst_idx:
        orig_row = test_idx[idx]
        print(f"  Predicted=${predictions_dollars[idx]:,.0f}  "
              f"Actual=${actual_dollars[idx]:,.0f}  "
              f"Error=${residuals[idx]:,.0f}")
        print(df.iloc[orig_row])
        print()

    # ---- Error graph 2: residual (error) distribution ----
    plt.clf()
    plt.hist(residuals, bins=30)
    plt.xlabel("Prediction error ($)  [predicted − actual]")
    plt.ylabel("Count")
    plt.title("Residual distribution — NC Housing test set")
    _output(plt, "nc_housing_residuals.png", show)


def _output(plt, filename, show):
    if show:
        plt.show()
    else:
        plt.savefig(filename, dpi=120, bbox_inches="tight")
        print(f"Saved plot to {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        default="project/NC_Housing_Prices_ready.csv",
        help="Path to the NC Housing CSV.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Open plot windows instead of saving PNG files.",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run far fewer epochs for a fast smoke test.",
    )
    parser.add_argument(
        "--final-epochs",
        type=int,
        default=None,
        help="Epoch count for the final model, once you've read your own turnaround epoch off the truncated curve.",
    )
    args = parser.parse_args()
    if not args.show:
        matplotlib.use("Agg")
    main(args.data, show=args.show, quick=args.quick, final_epochs=args.final_epochs)