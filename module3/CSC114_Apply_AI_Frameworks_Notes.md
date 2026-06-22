# CSC 114 — Apply AI Frameworks
## Working Notes & Build Log

> Living document — we'll keep filling this in as the model gets built, trained, and tested. Sections marked **TBD** get completed once we run the code in Colab.

---

## Course Context

- **Course:** CSC 114 – Artificial Intelligence I · FTCC · Section 1001 · Summer 2026
- **Assignment:** Apply AI Frameworks — **due 6/21/26** (100 pts)
- **Related:** Assess AI Frameworks, also due 6/21/26
- **Submission requirements:** `.py` file(s) + a text document answering the reflection questions below

---

## Assignment Instructions (as given)

For this assignment, work with your agent/project created for CSC-114 to help build a small custom AI model.

- Use the **Keras** Python library with a backend of your choice (TensorFlow, PyTorch, JAX).
- May need to train in **Google Colab** (training can be GPU/CPU intensive).
- Ask your agent about topics for the model — what dataset, what target to predict.
- The model must predict either a **number (regression)** or a **category (classification)**.
- Use a dataset that **already exists and is pre-cleaned**.
- Once done, have your agent explain what's happening in the code, and answer the following in a submitted text document:

  1. What are the different attributes of your dataset? What is the target value?
  2. Is the model regression or classification?
  3. What kind of optimizer was used to train your model? Why?
  4. How many epochs of training were required to get your model to predict the most optimal target value?
  5. What was the most accuracy (lowest loss) achieved by your model?
  6. Are you able to save your model, send it inputs, and get a prediction?
  7. Include anything else you think is relevant.

- **Submit:** your `.py` files and your text document.

---

## Decisions Made

| Choice | Pick | Why |
|---|---|---|
| **Backend** | PyTorch | Easiest of the three to debug, biggest tutorial/community base — best for a first build. (Default with no setup is TensorFlow; JAX is fastest but has the steepest learning curve.) |
| **Problem type** | Classification (multi-class, 10 categories) | "Accuracy" is a native, intuitive metric for classification — matches how the reflection questions are phrased. |
| **Dataset** | MNIST handwritten digits | Built into Keras, already split train/test, already labeled, no cleanup needed. Sets up nicely for the Computer Vision module later (7/12). |

---

## Build Log

### Step 1 — Build: load data & define the model architecture ✅

```python
import os
os.environ["KERAS_BACKEND"] = "torch"
import keras
from keras import layers

# MNIST comes pre-split into train/test, already labeled
(train_images, train_labels), (test_images, test_labels) = keras.datasets.mnist.load_data()

# Flatten each 28x28 image into one 784-number row, scale 0-255 down to 0-1
train_images = train_images.reshape((60000, 28 * 28)).astype("float32") / 255
test_images = test_images.reshape((10000, 28 * 28)).astype("float32") / 255

model = keras.Sequential([
    layers.Dense(512, activation="relu"),
    layers.Dense(10, activation="softmax"),
])
```

**Notes for the writeup:**
- **Attributes (features):** 784 pixel brightness values per image (28×28 grayscale, flattened).
- **Target:** a digit, 0–9 → 10 possible categories.
- **Why `Dense` layers:** the image was flattened into a plain list of numbers, so there's no spatial structure left for `Conv2D` to exploit (that comes later, in the Computer Vision module).
- **Why 10 output units + `softmax`:** one output per digit; softmax turns raw scores into probabilities across all 10 digits that sum to 1. Highest probability = the model's guess.
- **Why scale pixels to 0–1:** training is smoother and more stable on small, consistent number ranges than on raw 0–255 values.

### Step 2 — Compile: choose loss, optimizer, metrics ✅

```python
model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])
```

**Notes for the writeup:**
- **`optimizer="adam"`** — adaptive step size per parameter; the course's Module 3 reading calls it "the usual default — start here." Low-maintenance, no manual learning-rate tuning needed for a first model.
- **`loss="sparse_categorical_crossentropy"`** — crossentropy because this is multi-class classification (10 categories), not regression (which would use MSE). "Sparse" specifically because our labels are plain integers (`5`, `0`, `9`...) rather than one-hot vectors — if they were one-hot, we'd use `categorical_crossentropy` instead.
- **`metrics=["accuracy"]`** — doesn't affect training (only the loss does that); it's just a human-readable score for us to monitor.

### Step 3 — Fit: train the model ✅

```python
# Save ONLY the most accurate model so far, judged by validation accuracy.
checkpoint = keras.callbacks.ModelCheckpoint(
    filepath="mnist_best_model.keras",
    monitor="val_accuracy", mode="max",
    save_best_only=True, verbose=1)

history = model.fit(train_images, train_labels,
                    epochs=20, batch_size=128,
                    validation_data=(test_images, test_labels),
                    callbacks=[checkpoint])
```

**What happened (run in the codespace, PyTorch backend):**
- Trained for 20 epochs, batch size 128. A custom callback printed each epoch's loss, accuracy, and **error rate** (error = 1 − accuracy).
- Validation accuracy climbed, then peaked and plateaued — classic mild overfitting after the best epoch:

  | Epoch | val_acc | val_err | note |
  |---|---|---|---|
  | 13 | 0.9835 | 0.0165 | improved, saved |
  | **15** | **0.9838** | **0.0162** | **best — saved** |
  | 16 | 0.9834 | 0.0166 | no improvement |
  | 20 | 0.9817 | 0.0183 | no improvement |

- **Best epoch:** 15 · **best validation accuracy:** 0.9838 (98.38%) · **lowest error rate:** 0.0162 (1.62%) · **loss at best epoch:** 0.0637.
- `save_best_only=True` means the file on disk (`mnist_best_model.keras`) is always the single most accurate version, not the last epoch.

### Step 4 — Predict: test it on new data, save/load ✅

```python
best_model = keras.models.load_model("mnist_best_model.keras")
probabilities = best_model.predict(test_images[:1])
predicted_digit = int(probabilities.argmax(axis=1)[0])
```

**What happened:**
- Reloaded the saved best model and predicted on one test image → **predicted digit 7, actual 7, confidence 1.0000.**
- Confirms the full save → load → predict round-trip works.

---

## Reflection Question Drafts

1. **Attributes / target:** 784 grayscale pixel values per image (28×28 flattened); target is the digit label, 0–9.
2. **Regression or classification:** Classification (multi-class, 10 categories).
3. **Optimizer used / why:** Adam — adaptive per-parameter step sizes, the course material's recommended default for a first model; no manual learning-rate tuning required.
4. **Epochs needed for best result:** 15 epochs. Validation accuracy peaked at epoch 15; training to 20 epochs did not improve it (the model began to overfit — training accuracy kept rising while validation accuracy drifted down).
5. **Best accuracy / lowest loss achieved:** 98.38% validation accuracy (error rate 1.62%), with a loss of 0.0637 at that epoch.
6. **Save model / predict on new input:** Yes. The most accurate model is saved to `mnist_best_model.keras` via `ModelCheckpoint(save_best_only=True)`, then reloaded with `keras.models.load_model(...)` and used to predict. On a test image it predicted digit 7 (actual 7) with 1.0000 confidence.
7. **Anything else relevant:** Used `ModelCheckpoint` monitoring `val_accuracy` so only the single best version is kept, not the final (overfit) one. A custom callback prints every epoch's loss, accuracy, and error rate to the screen. Trained locally in the codespace on the PyTorch backend (no GPU needed for this small dense network).

---

## Submission Checklist

- [x] `.py` file(s) with the full working model — `model.py`
- [x] Text document with all reflection answers filled in
