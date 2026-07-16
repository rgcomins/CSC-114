"""
CSC-114 Module 5/6 — NC Housing Price Regression (Housing Reskin)  ·  v2
=======================================================================

Adapted from *Deep Learning with Python*, 3rd Ed., Chapter 4, Example 3
(California Housing scalar regression), reskinned onto the NC Housing dataset
(D. Michael Senter, ACS 2018 5-year estimates). Predictions are at the census
block-group (neighborhood) level, not individual homes.

THE WORKFLOW (one machine-learning step per section, top to bottom):
    load -> clean -> split -> normalize/scale -> K-fold validation
         -> read the curve -> train final model -> evaluate -> predict
         -> error diagnostics

WHAT'S NEW IN v2 (vs. v1):
    1. Fuller inline documentation so the script reads cleanly when presented.
    2. Every artifact a run produces — all PNG plots AND a full copy of the
       console output — is written to a timestamped file. A new run never
       overwrites an old one, and nothing has to be hand-saved.
    3. The model itself is UNCHANGED from v1. The "one change" experiment
       comes later, once we've confirmed v2 behaves exactly like v1.

Run:
    python nc_housing_model_v2.py                  # save timestamped PNGs + log
    python nc_housing_model_v2.py --show           # open plot windows instead
    python nc_housing_model_v2.py --quick          # fewer epochs, fast smoke test
    python nc_housing_model_v2.py --data path.csv  # point at a specific CSV
    python nc_housing_model_v2.py --outdir runs    # choose where files land

Data: a cleaned NC Housing CSV. See the KNOWN NAMING ITEMS note near the
      bottom before reconciling filenames — a couple of naming mismatches are
      carried over from v1 on purpose and left for a later cleanup pass.
"""

import argparse
import os
import sys
from datetime import datetime

# KERAS_BACKEND must be set BEFORE keras is imported. "torch" matches the class
# stack; setdefault means an env var set outside the script still wins.
os.environ.setdefault("KERAS_BACKEND", "torch")

import numpy as np
import pandas as pd
import matplotlib

import keras
from keras import layers


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TARGET_COL = "median_house_value"       # the number we're predicting (a dollar amount)
TARGET_SCALE = 100_000                   # same convention as the CA Housing example;
                                         # sanity-checked against the data at runtime below

# Only these columns are trusted from the raw CSV. Anything else in the file —
# the phantom "Unnamed: N" columns that trailing commas create, or any column
# we haven't vetted — is never loaded, because usecols=KEEP_COLS filters the
# read itself (see load_and_clean). Filtering at read time means junk columns
# can't sneak in and quietly break a later dropna().
#
# NOTE (unchanged from v1 on purpose): this list carries "total_rooms". In the
# source file, total_rooms and total_bedrooms are identical duplicates, so which
# of the two names appears here changes no numbers — it's a labeling question,
# and we're deliberately leaving it alone until the post-v2 "one change" step.
KEEP_COLS = [
    "population",
    "households",
    "median_income",
    "median_house_value",
    "total_rooms",
    "latitude",
    "longitude",
    "housing_median_age",
]


# ---------------------------------------------------------------------------
# Timestamped-output helpers (the v2 feature)
# ---------------------------------------------------------------------------

def run_timestamp():
    """Return one stamp per run, e.g. '20260716_143022'.

    Computed ONCE and reused for every file the run writes, so all of a run's
    outputs share the same suffix and group together on disk. The format has no
    ':' or spaces (safe as a filename on every OS) and sorts chronologically,
    so the newest run is always last alphabetically.
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def stamped_path(outdir, basename, stamp, ext):
    """Build 'outdir/basename_stamp.ext' — a datetime-appended output path."""
    return os.path.join(outdir, f"{basename}_{stamp}.{ext}")


class _Tee:
    """A fan-out stream: everything written here goes to the real console AND a
    log file at the same time.

    We point sys.stdout at one of these, so every existing print() (and Keras's
    own progress output) is captured into the run log with no other code
    changes. Flushing on each write keeps the on-disk log current even if the
    run is interrupted partway through.
    """

    def __init__(self, *streams):
        self._streams = streams

    def write(self, data):
        for s in self._streams:
            s.write(data)
            s.flush()
        return len(data)

    def flush(self):
        for s in self._streams:
            s.flush()


# ---------------------------------------------------------------------------
# Data loading + cleaning
# ---------------------------------------------------------------------------

def load_and_clean(path):
    """Load the trusted columns and drop the known-bad rows in this specific
    file. This is a targeted cleanup of one dataset, not a general pipeline."""
    # usecols restricts the read to exactly the trusted columns, so phantom
    # "Unnamed: N" columns from trailing commas never enter the DataFrame.
    df = pd.read_csv(path, usecols=KEEP_COLS)
    print("Raw rows:", len(df))
    print("Raw columns:", list(df.columns))

    # Drop rows where the target is missing or is the 9999 placeholder sentinel.
    df = df[df[TARGET_COL].notna()]
    df = df[df[TARGET_COL] != 9999]
    print("After dropping missing/9999 target rows:", len(df))

    # Drop the bad housing_median_age == 2018 rows (a stray median-year-built
    # value that leaked in as an age). Removing beats "correcting" — repairing
    # to a guessed value would assert information we don't actually have.
    if "housing_median_age" in df.columns:
        df = df[df["housing_median_age"] != 2018]
    print("After dropping bad housing_median_age rows:", len(df))

    # Sweep up any remaining rows with missing values anywhere.
    df = df.dropna()
    print("After dropping remaining NaNs:", len(df))

    return df


# ---------------------------------------------------------------------------
# Model (UNCHANGED from v1 — do not touch until the "one change" step)
# ---------------------------------------------------------------------------

def get_model(input_dim):
    """Small feed-forward regressor: two 64-unit ReLU layers, one linear output.

    - Small on purpose: a small dataset overfits less with a small model.
    - The final Dense(1) has NO activation, so it can output any dollar value.
    - Loss is MSE (what training minimizes); MAE is the human-readable metric
      (average dollars off, once we multiply back by TARGET_SCALE).
    - Regression has no "accuracy" — that's a classification idea.
    """
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


# ---------------------------------------------------------------------------
# Main workflow
# ---------------------------------------------------------------------------

def main(data_path, outdir, stamp, show=False, quick=False, final_epochs=None):
    import matplotlib.pyplot as plt

    # ---- Load and clean the NC Housing dataset ----
    df = load_and_clean(data_path)

    feature_cols = [c for c in df.columns if c != TARGET_COL]
    print("Features used:", feature_cols)

    # Features (the inputs the model gets to see) and target (what it predicts).
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

    # ---- Prepare the data: normalize features (TRAIN stats only), scale targets ----
    # Normalizing with the test set's own statistics would leak information from
    # the test set into training — so mean/std come from the training split only.
    mean = train_data.mean(axis=0)
    std = train_data.std(axis=0)
    x_train = (train_data - mean) / std
    x_test = (test_data - mean) / std

    # Scale targets into a small range; we multiply predictions back by
    # TARGET_SCALE later to read them as dollars.
    y_train = train_targets / TARGET_SCALE
    y_test = test_targets / TARGET_SCALE

    # ---- K-fold validation, pass 1: a single average validation score ----
    # The dataset is small enough that one train/val split would swing depending
    # on which rows got held out. K-fold runs K models, each leaving out a
    # different slice, and averages — a steadier read on how the setup
    # generalizes. This runs inside the 80% training pool, before the final fit.
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

    # ---- K-fold validation, pass 2: full per-epoch MAE history ----
    # Same folds, but this time we keep the validation MAE at every epoch so we
    # can plot the curve and find where it stops improving (the turnaround).
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

    # Average the per-epoch validation MAE across all K folds.
    average_mae_history = [
        np.mean([h[i] for h in all_mae_histories]) for i in range(num_epochs)
    ]

    # Plot the full validation MAE curve (scaled units, matching the book).
    val_mae_path = stamped_path(outdir, "nc_housing_val_mae", stamp, "png")
    epochs = range(1, len(average_mae_history) + 1)
    plt.plot(epochs, average_mae_history)
    plt.xlabel("Epochs")
    plt.ylabel("Validation MAE (scaled)")
    plt.title("Average validation MAE per epoch — NC Housing")
    _output(plt, val_mae_path, show)

    # Same curve with the first 10 (noisy, high-MAE) epochs dropped. THIS is the
    # one to read for the turnaround epoch — don't take the default on faith.
    plt.clf()
    val_mae_trunc_path = stamped_path(outdir, "nc_housing_val_mae_truncated", stamp, "png")
    truncated_mae_history = average_mae_history[10:]
    epochs = range(10, len(truncated_mae_history) + 10)
    plt.plot(epochs, truncated_mae_history)
    plt.xlabel("Epochs")
    plt.ylabel("Validation MAE (scaled)")
    plt.title("Average validation MAE (first 10 epochs dropped) — NC Housing")
    _output(plt, val_mae_trunc_path, show)

    # ---- Train the final model and evaluate on the held-out test set ----
    # final_epochs is a placeholder until you read your OWN turnaround epoch off
    # the truncated curve above and pass it with --final-epochs N.
    epochs_to_use = final_epochs or (30 if quick else 50)
    model = get_model(x_train.shape[1])
    model.fit(x_train, y_train, epochs=epochs_to_use, batch_size=16, verbose=0)
    test_mse, test_mae = model.evaluate(x_test, y_test)
    print(f"Test MAE (scaled): {test_mae:.3f}  ->  ${test_mae * TARGET_SCALE:,.0f} off, on average")

    # ---- Generate predictions on the test set, converted back to dollars ----
    predictions_scaled = model.predict(x_test)
    predictions_dollars = predictions_scaled.flatten() * TARGET_SCALE
    actual_dollars = y_test * TARGET_SCALE

    print("\nFirst 5 test predictions vs. actual:")
    for pred, actual in zip(predictions_dollars[:5], actual_dollars[:5]):
        print(f"  Predicted: ${pred:,.0f}   Actual: ${actual:,.0f}   Error: ${pred - actual:,.0f}")

    # ---- Error graph 1: predicted vs. actual scatter ----
    # Points on the red dashed line are perfect; spread around it is the error.
    plt.clf()
    pred_vs_actual_path = stamped_path(outdir, "nc_housing_pred_vs_actual", stamp, "png")
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
    _output(plt, pred_vs_actual_path, show)

    residuals = predictions_dollars - actual_dollars

    # ---- Diagnostic: inspect the worst residuals (data vs. model check) ----
    # Print the largest misses and their raw feature rows, so we can tell a
    # genuinely hard case apart from a bad data row.
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
    # A roughly centered, symmetric histogram means no systematic over/under-bias.
    plt.clf()
    residuals_path = stamped_path(outdir, "nc_housing_residuals", stamp, "png")
    plt.hist(residuals, bins=30)
    plt.xlabel("Prediction error ($)  [predicted - actual]")
    plt.ylabel("Count")
    plt.title("Residual distribution — NC Housing test set")
    _output(plt, residuals_path, show)


def _output(plt, path, show):
    """Either display the current figure (--show) or save it to `path`."""
    if show:
        plt.show()
    else:
        plt.savefig(path, dpi=120, bbox_inches="tight")
        print(f"Saved plot to {path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
#
# KNOWN NAMING ITEMS (carried over from v1, intentionally NOT changed here):
#   - The --data default filename and the "cleaned CSV" name we've used
#     elsewhere (NC_Housing_Prices_2018_age_cleaned.csv) don't match. Left as-is
#     so v2 runs identically to v1; reconcile deliberately in a later pass.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="NC Housing price regression (CSC-114 Module 5/6), v2."
    )
    parser.add_argument(
        "--data",
        default="project/NC_Housing_Prices_ready.csv",
        help="Path to the NC Housing CSV.",
    )
    parser.add_argument(
        "--outdir",
        default="outputs",
        help="Directory for timestamped plots and the run log (created if "
             "missing). Use '.' for the current folder.",
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
        help="Epoch count for the final model, once you've read your own "
             "turnaround epoch off the truncated curve.",
    )
    args = parser.parse_args()

    if not args.show:
        matplotlib.use("Agg")  # headless backend so savefig works in a Codespace

    # ---- One timestamp + one output folder for the whole run ----
    stamp = run_timestamp()
    os.makedirs(args.outdir, exist_ok=True)

    # ---- Mirror all console output into a timestamped log file ----
    # Every print() and Keras progress line from this run is preserved on disk.
    log_path = stamped_path(args.outdir, "run_log", stamp, "txt")
    log_file = open(log_path, "w", encoding="utf-8")
    original_stdout = sys.stdout
    sys.stdout = _Tee(original_stdout, log_file)

    try:
        print(f"Run timestamp: {stamp}")
        print(f"Writing plots and this log to: {os.path.abspath(args.outdir)}")
        print(f"Console log: {log_path}\n")
        main(
            args.data,
            args.outdir,
            stamp,
            show=args.show,
            quick=args.quick,
            final_epochs=args.final_epochs,
        )
    finally:
        # Restore stdout and close the log no matter how the run ends.
        sys.stdout = original_stdout
        log_file.close()
        print(f"\nDone. Full console log saved to {log_path}")
