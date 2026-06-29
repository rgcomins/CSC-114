# Ground Truth — California Housing Prices (Scalar Regression)

**CSC-114 · Module 4 (Chapter 4) · Reference spec for you and your AI assistant**

Use this as the *source of truth* when you and your agent build the housing example. If your agent contradicts this page, trust this page (and ask the agent why it disagreed).

> **Note:** Older editions of this book used a Boston housing dataset. The 3rd edition replaced it with **California Housing**, which is what you'll use here.

---

## The problem in one sentence

Given eight facts about a California district, predict the **median home price** for that district — a continuous dollar amount. Predicting a number (not a category) → this is **scalar regression**.

---

## The data

- The **California Housing** dataset ships inside Keras. It comes from the 1990 U.S. census; each row is a "block group" (think: a small district).
- Use the **small version on purpose** — only 600 districts (480 train / 120 test). Real datasets are often tiny, and you need to know how to handle that.
- **8 features per district:** longitude, latitude, median house age, total rooms, total bedrooms, population, households, median income.
- **Target:** median home value in dollars, ranging roughly **$60,000–$500,000** (1990 prices, not inflation-adjusted).

```python
from keras.datasets import california_housing

# version="small" is required to get the 600-district set.
(train_data, train_targets), (test_data, test_targets) = (
    california_housing.load_data(version="small")
)
# train_data.shape -> (480, 8)   test_data.shape -> (120, 8)
```

---

## The pipeline (the shape of the whole job)

1. **Load** the data (`version="small"`).
2. **Normalize the features** — center each column at 0 with unit spread, using **training stats only.**
3. **Scale the targets** — divide by 100,000 so prices sit in a small range (0.6 to 5).
4. **Build** the model.
5. **Compile** (MSE loss, MAE metric).
6. **Validate with K-fold** (data is too small for one trustworthy split).
7. **Read the curve**, pick a good number of epochs, train a final model on all the data.
8. **Evaluate** on the test set, then **predict**.

```python
# Normalize features using TRAINING mean/std only — never the test set's.
mean = train_data.mean(axis=0)
std = train_data.std(axis=0)
x_train = (train_data - mean) / std
x_test = (test_data - mean) / std

# Scale targets into a small range. Multiply predictions back by 100,000 later.
y_train = train_targets / 100000
y_test = test_targets / 100000
```

---

## The model

Small, because the dataset is small (small models overfit less on little data):

```python
import keras
from keras import layers

def get_model():
    model = keras.Sequential([
        layers.Dense(64, activation="relu"),
        layers.Dense(64, activation="relu"),
        layers.Dense(1),                # no activation — a linear output
    ])
    model.compile(
        optimizer="adam",
        loss="mean_squared_error",
        metrics=["mean_absolute_error"],
    )
    return model
```

- The last layer has **no activation** — it's purely linear so the model can output **any** dollar value. (A `sigmoid` here would trap the output between 0 and 1.)
- **MSE (mean squared error)** is the loss; **MAE (mean absolute error)** is the friendly metric — an MAE of 0.5 means "off by about $50,000 on average," because targets were scaled by 100,000.
- **There is no "accuracy" in regression.** Accuracy is a classification idea.

---

## Validation and the overfitting story

With only ~480 training points, a single validation split is unreliable — the score swings depending on *which* points you held out. The fix is **K-fold cross-validation** (here, K = 4): split into 4 parts, train 4 models each leaving one part out, average the scores.

- At **50 epochs**, the average validation MAE is about **0.296 → ~$29,600 off.**
- Train longer (200 epochs) and plot the per-epoch MAE: it stops improving around **120–140 epochs**, then starts overfitting.
- Train a final model on all training data for ~130 epochs, then evaluate:

```python
model = get_model()
model.fit(x_train, y_train, epochs=130, batch_size=16, verbose=0)
test_mse, test_mae = model.evaluate(x_test, y_test)   # MAE ≈ 0.31 → ~$31,000 off

predictions = model.predict(x_test)
# predictions are in hundreds of thousands, e.g. 2.83 -> about $283,000
```

---

## Things your AI assistant often gets wrong (watch for these)

| Trap | The truth |
|---|---|
| Adds `metrics=["accuracy"]` | Regression has **no accuracy** — use **MAE** (and MSE as loss). |
| Puts an activation on the last layer | The output layer is **linear (no activation)** so it can predict any dollar value. |
| Normalizes using the **test set's** mean/std | Use **training** stats only — test stats leaking in is cheating. |
| Forgets to **scale the targets** (or to scale predictions back) | Divide targets by 100,000; multiply predictions by 100,000 to read dollars. |
| Uses a single train/val split | Data is tiny — use **K-fold** so the score is trustworthy. |
| "More epochs = better" | Validation MAE flattens ~120–140 epochs, then overfits. |

---

## Numbers you should be able to reproduce (roughly)

- Training samples: **480** · Features: **8**
- K-fold (K=4) average MAE at 50 epochs: **~0.296 (~$29,600)**
- Overfitting begins: **~120–140 epochs**
- Final test MAE (~130 epochs): **~0.31 (~$31,000)**

---

*Source: François Chollet & Matthew Watson, "Deep Learning with Python," 3rd Edition (Manning), Chapter 4 — free online at deeplearningwithpython.io. Code shown is standard Keras API usage for reference. Your exact numbers will vary slightly due to random initialization.*
