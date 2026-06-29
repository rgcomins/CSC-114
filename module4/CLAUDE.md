# CLAUDE.md — Module 4: California Housing Regression

## Mission

Build a working California Housing price prediction model (scalar regression) using Keras with the PyTorch backend. This is the Module 4 "Apply Classification & Regression" assignment for CSC-114.

**Priority: get a working baseline that meets all four submission criteria. Do not optimize or tweak until the baseline is confirmed working.**

---

## Environment

- GitHub Codespaces (Linux)
- Keras 3 with PyTorch backend
- **CRITICAL:** Set `KERAS_BACKEND` before any keras import. We learned this the hard way in Module 3 — TF/PyTorch backend collision causes a segfault.

```python
import os
os.environ["KERAS_BACKEND"] = "torch"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
```

---

## Submission Criteria (all four required)

1. Code runs end to end without errors
2. Model trains and loss goes DOWN over epochs
3. A training-vs-validation MAE curve is saved as an image file
4. The overfitting turnaround epoch is identifiable from the curve

---

## Build Phases

### Phase 1 — Load & Prep (`california_housing_regression.py`)

```python
from keras.datasets import california_housing

(train_data, train_targets), (test_data, test_targets) = (
    california_housing.load_data(version="small")
)
# Expected: train_data.shape -> (480, 8), test_data.shape -> (120, 8)
```

**Normalize features — training stats ONLY:**
```python
mean = train_data.mean(axis=0)
std = train_data.std(axis=0)
x_train = (train_data - mean) / std
x_test = (test_data - mean) / std
```

**Scale targets:**
```python
y_train = train_targets / 100000
y_test = test_targets / 100000
```

⚠️ TRAPS TO AVOID:
- Do NOT normalize using test set statistics — that leaks future data
- Do NOT forget to scale targets — raw dollar values in the hundreds of thousands will destabilize training
- Remember to multiply predictions back by 100,000 when displaying dollar amounts

### Phase 2 — Build & Compile

```python
import keras
from keras import layers

def get_model():
    model = keras.Sequential([
        layers.Dense(64, activation="relu"),
        layers.Dense(64, activation="relu"),
        layers.Dense(1),  # NO activation — linear output for regression
    ])
    model.compile(
        optimizer="adam",
        loss="mean_squared_error",
        metrics=["mean_absolute_error"],
    )
    return model
```

⚠️ TRAPS TO AVOID:
- Do NOT add `metrics=["accuracy"]` — accuracy does not exist in regression. Use MAE.
- Do NOT put an activation on the final Dense(1) layer — sigmoid would trap output between 0 and 1, relu would block negative corrections. Linear output lets the model predict any value.

### Phase 3 — K-Fold Cross-Validation + Training Curve

Use K=4 folds. The dataset is too small (480 samples) for a single train/val split to be trustworthy.

```python
import numpy as np

k = 4
num_val_samples = len(x_train) // k
num_epochs = 200
all_mae_histories = []

for i in range(k):
    print(f"Processing fold #{i}")
    
    # Carve out validation fold
    val_data = x_train[i * num_val_samples: (i + 1) * num_val_samples]
    val_targets = y_train[i * num_val_samples: (i + 1) * num_val_samples]
    
    # Everything else is training
    partial_train_data = np.concatenate(
        [x_train[:i * num_val_samples],
         x_train[(i + 1) * num_val_samples:]],
        axis=0)
    partial_train_targets = np.concatenate(
        [y_train[:i * num_val_samples],
         y_train[(i + 1) * num_val_samples:]],
        axis=0)
    
    # Fresh model each fold
    model = get_model()
    history = model.fit(partial_train_data, partial_train_targets,
                        validation_data=(val_data, val_targets),
                        epochs=num_epochs, batch_size=16, verbose=0)
    
    mae_history = history.history["val_mean_absolute_error"]
    all_mae_histories.append(mae_history)

# Average MAE across folds per epoch
average_mae_history = [
    np.mean([x[i] for x in all_mae_histories]) for i in range(num_epochs)
]
```

### Phase 4 — Plot and Save the Training Curve

This is a required deliverable. Save as a file — do not just plt.show().

```python
import matplotlib.pyplot as plt

# Smooth the curve by dropping the first 10 epochs (noisy) 
# and plotting an exponential moving average
def smooth_curve(points, factor=0.9):
    smoothed = []
    for point in points:
        if smoothed:
            previous = smoothed[-1]
            smoothed.append(previous * factor + point * (1 - factor))
        else:
            smoothed.append(point)
    return smoothed

smooth_mae = smooth_curve(average_mae_history[10:])

plt.figure(figsize=(10, 6))
plt.plot(range(10, num_epochs), smooth_mae, label="Smoothed K-fold avg validation MAE")
plt.xlabel("Epochs")
plt.ylabel("Validation MAE (scaled)")
plt.title("California Housing — K-Fold Validation MAE")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("training_curve.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: training_curve.png")
```

**Expected result:** MAE drops steeply for ~50 epochs, flattens around 120–140, then starts creeping up (overfitting). The turnaround epoch is approximately 120–140.

### Phase 5 — Train Final Model & Evaluate

After identifying the turnaround from the curve, train one final model on ALL training data for that many epochs:

```python
final_epochs = 130  # adjust based on what the curve actually shows

model = get_model()
model.fit(x_train, y_train, epochs=final_epochs, batch_size=16, verbose=0)

test_mse, test_mae = model.evaluate(x_test, y_test)
print(f"Test MSE: {test_mse:.4f}")
print(f"Test MAE: {test_mae:.4f} (≈ ${test_mae * 100000:,.0f} avg error)")
```

**Expected:** Test MAE ≈ 0.31 → approximately $31,000 average prediction error.

### Phase 6 — Sample Predictions

Show a few predictions vs. actuals so we can sanity-check:

```python
predictions = model.predict(x_test[:5])
for i in range(5):
    predicted = predictions[i][0] * 100000
    actual = y_test[i] * 100000
    print(f"District {i}: Predicted ${predicted:,.0f} | Actual ${actual:,.0f} | Off by ${abs(predicted - actual):,.0f}")
```

### Phase 7 — Save the Model

```python
model.save("california_housing_model.keras")
print("Model saved: california_housing_model.keras")
```

---

## Deliverables Checklist

- [ ] `california_housing_regression.py` — complete script, runs end to end
- [ ] `training_curve.png` — saved K-fold validation MAE plot
- [ ] Console output showing: loss decreasing, final test MAE, sample predictions
- [ ] Note the overfitting turnaround epoch (for use in the Assess task)

---

## What NOT to Do

- Do not use accuracy as a metric (this is regression, not classification)
- Do not put an activation function on the output layer
- Do not normalize with test set statistics
- Do not use a single train/val split (K-fold is required for this dataset size)
- Do not skip saving the training curve image — it's a hard requirement
- Do not tweak the model yet — get baseline working first, then we'll add one change
