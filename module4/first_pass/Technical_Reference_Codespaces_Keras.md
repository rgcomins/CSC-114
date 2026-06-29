# Session Technical Reference: Codespaces, Claude Code & Keras/PyTorch
**CSC 114 — For the Programmers**
*Based on: claude_code_session_notes_full.md*

---

## 1. Installing Claude Code

Two install paths exist. The native installer is preferred because it bundles its own Node.js runtime — nothing to manage separately.

```bash
# Recommended — no Node.js required
curl -fsSL https://claude.ai/install.sh | bash

# npm alternative (if you already have Node.js)
npm install -g @anthropic-ai/claude-code
```

**Hard rules:**
- Never `sudo npm install -g` anything. npm global installs with sudo corrupt permission trees on Linux/macOS.
- Requires an active Claude account: Pro, Max, Teams, Enterprise, or API Console.

---

## 2. Bash Environment Variables — The Right Way

Three ways to inspect a variable:

```bash
echo $VARIABLE_NAME         # basic
echo "$MY_VAR"              # safer: double-quotes preserve whitespace and newlines
declare -p MY_VAR           # shows type info + value; useful for debugging
```

**The critical distinction — local vs. exported:**

```bash
MY_VAR="hello"              # local to current shell only — child processes (Python, etc.) cannot see it
export MY_VAR="hello"       # inherited by all child processes
```

This distinction is why `import os; os.environ.get("MY_VAR")` can return `None` even when you *know* you set the variable — if you forgot `export`, Python never received it.

---

## 3. Testing the Anthropic API

Minimal smoke test:

```python
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment automatically

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=32,
    messages=[{"role": "user", "content": "Say 'API connection successful!'"}]
)

print(response.content[0].text)
```

If this throws an `AuthenticationError`, the key isn't in the environment. If it throws a `ConnectionError`, check network/proxy. A clean print means the full stack is live.

---

## 4. API Key Persistence — The Problem and All Three Fixes

**What happened:** Installing the VS Code Python extension triggered a full window reload. That reload spun up a fresh terminal, wiping all `export` statements from the previous session. `ANTHROPIC_API_KEY` disappeared.

**Diagnostic:**
```bash
echo $ANTHROPIC_API_KEY
python -c "import os; print(os.environ.get('ANTHROPIC_API_KEY', 'NOT FOUND'))"
```

**Fix tier 1 — Persist in `~/.bashrc` (survives terminal restarts):**
```bash
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc     # apply immediately to current session
```
This works until the Codespace VM itself is rebuilt.

**Fix tier 2 — GitHub Codespace Secrets (survives everything):**
`GitHub → Settings → Codespaces → New secret → Name: ANTHROPIC_API_KEY`

Secrets are injected as environment variables at Codespace startup. They survive window reloads, terminal restarts, and full Codespace rebuilds. This is the correct long-term solution.

**Security reminder:** Never paste an API key in plain text in a chat, commit, or shared doc. If a key is exposed, revoke it immediately at `console.anthropic.com` and generate a new one.

---

## 5. Running Claude Code

```bash
claude                               # start interactive session
claude "fix the bug in script.py"   # one-shot task, exits when done
claude -p "describe this function"  # non-interactive, prints output and exits
claude --help                       # full option reference
```

The interactive session (`claude` with no args) is most useful for multi-step work — it maintains conversation context across tool calls.

---

## 6. The MNIST Keras Model — Layer by Layer

```python
model = keras.Sequential([
    layers.Dense(512, activation="relu"),
    layers.Dense(10, activation="softmax"),
])
```

**Layer 1: `Dense(512, activation="relu")`**
- 512 neurons, fully connected to the 784 input features (28×28 flattened pixel values).
- ReLU activation: `f(x) = max(0, x)`. Negative values become zero; positive values pass through unchanged. This is the standard choice for hidden layers because it's computationally cheap and avoids vanishing gradients.
- This layer learns *which combinations of pixel values matter* for distinguishing digits.

**Layer 2: `Dense(10, activation="softmax")`**
- 10 neurons, one per digit class (0–9).
- Softmax converts raw scores (logits) into a probability distribution that sums to exactly 1.0:

```
Input logits:    [2.1,  0.3,  0.1,  0.4,  0.2,  0.1,  0.2,  3.8,  0.3,  0.2]
After softmax:   [0.02, 0.01, 0.01, 0.03, 0.01, 0.02, 0.01, 0.85, 0.02, 0.02]
                                                                 ↑
                                                        85% → class 7 (prediction)
```

`prediction.argmax()` extracts the index of the highest probability — that's the predicted digit.

---

## 7. Epochs and Early Stopping

By default, `model.fit(epochs=N)` runs all N epochs regardless of whether the model has stopped improving. Early stopping adds a watchdog:

```python
from tensorflow.keras.callbacks import EarlyStopping

early_stop = EarlyStopping(
    monitor="val_loss",           # watch validation loss (not training loss)
    patience=5,                   # tolerate 5 epochs of no improvement before stopping
    restore_best_weights=True     # roll back to the epoch with the lowest val_loss on stop
)

model.fit(
    x_train, y_train,
    epochs=50,
    validation_data=(x_val, y_val),
    callbacks=[early_stop]
)
```

`patience` is the key tuning parameter. Too low (e.g., 2) and you stop during normal training noise. Too high (e.g., 20) and you waste time in the flat zone after learning has plateaued. Five is a reasonable default for most MNIST-scale problems.

`restore_best_weights=True` means the final model weights come from the *best* epoch, not the last one. Without this, you might stop at epoch 22 when the best performance was at epoch 17.

---

## 8. Choosing the Number of Epochs — Learning Curves

Plot training loss vs. validation loss after every run:

```python
history = model.fit(...)

import matplotlib.pyplot as plt
plt.plot(history.history["loss"], label="train loss")
plt.plot(history.history["val_loss"], label="val loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.show()
```

**Three zones to recognize:**

| Zone | What the curves do | What it means |
|---|---|---|
| Learning | Both losses fall together | Model is genuinely improving — let it run |
| Sweet spot | Val loss flattens or starts a shallow rise | Stop here or let early stopping catch it |
| Overfitting | Train loss keeps falling, val loss rises | Model is memorizing training data — stop now |

**Starting-point rules of thumb by dataset size:**

| Dataset size | Initial epoch budget |
|---|---|
| Small (< 10k samples) | 50–100 |
| Medium (10k–100k) | 20–50 |
| Large (> 100k) | 10–20 |

Best practice: set a generous upper bound, enable early stopping with `restore_best_weights=True`, then use the learning curve plot to understand what actually happened.

---

## 9. The Segfault — Root Cause and Fix

**What happened:** The training script used `import keras` (standalone, PyTorch backend). The inference script used `from tensorflow import keras`. When the inference script ran, it initialized TensorFlow's runtime. TensorFlow's runtime and PyTorch's runtime both tried to claim the same GPU/memory resources simultaneously. The process crashed with a segmentation fault.

**Root cause in one line:** Two competing C++ runtimes (TF and PyTorch) both initializing in the same Python process.

**The fix:**

```python
import os
os.environ["KERAS_BACKEND"] = "torch"   # must be set BEFORE importing keras
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # suppress TF's noisy startup logs

import keras    # standalone keras — NOT: from tensorflow import keras
```

The `KERAS_BACKEND` environment variable must be set *before* any keras import. Once keras is imported, the backend is locked in for that process. Setting it afterward has no effect.

`TF_CPP_MIN_LOG_LEVEL = "3"` suppresses TensorFlow's C++ layer warnings even when TF isn't the active backend — it tends to log anyway if it's installed.

---

## 10. Final Inference Script — Annotated

```python
import os
os.environ["KERAS_BACKEND"] = "torch"     # lock in PyTorch backend before any keras import
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # silence TF noise

import keras
import numpy as np
import matplotlib.pyplot as plt

# Load the saved model
# compile=False skips loading optimizer state — avoids pulling in conflicting backend metadata
model = keras.models.load_model("mnist_best_model.keras", compile=False)

# Load MNIST test set (we don't need the training split here)
(_, _), (x_test, y_test) = keras.datasets.mnist.load_data()

# Select a single test image by index (0–9999)
index = 0
image = x_test[index]

# Preprocess to match training conditions
# - Cast to float32 (model expects floats, not uint8)
# - Normalize to [0, 1] (training data was normalized the same way)
# - Reshape from (28, 28) to (1, 784) — batch dimension + flattened
image_input = image.astype("float32") / 255.0
image_input = image_input.reshape(1, 784)

# Run inference
prediction = model.predict(image_input)   # returns shape (1, 10) — one probability per class
predicted_class = prediction.argmax()     # index of highest probability = predicted digit

# Save labeled visualization
# NOTE: predict() must run before savefig() — predicted_class must exist for the title string
plt.imshow(image, cmap="gray")
plt.title(f"Actual: {y_test[index]}  |  Predicted: {predicted_class}")
plt.axis("off")
plt.savefig("prediction.png", bbox_inches="tight")
plt.close()    # frees memory — important when saving many images in a loop

print(f"Predicted: {predicted_class}")
print(f"Actual:    {y_test[index]}")
```

**Key details that matter in practice:**

| Decision | Why it matters |
|---|---|
| `compile=False` on load | Skips optimizer metadata that would attempt to reinitialize conflicting backends |
| `astype("float32") / 255.0` | Must match exact preprocessing used during training — mismatched normalization degrades predictions silently |
| `reshape(1, 784)` | The leading `1` is the batch dimension; model always expects a batch, even for a single sample |
| `predict()` before `plt.title()` | `predicted_class` must exist before the f-string is evaluated |
| `plt.close()` | Without this, matplotlib accumulates figures in memory — harmless for one image, problematic in a loop |
| Change `index` to 0–9999 | Full MNIST test set has 10,000 images; any index in that range is valid |

---

## Quick Reference: Environment Setup Sequence

When starting a fresh Codespace session from scratch:

```bash
# 1. Verify API key is present
echo $ANTHROPIC_API_KEY

# 2. If missing, restore from ~/.bashrc
source ~/.bashrc

# 3. Confirm Python can see it
python -c "import os; print(os.environ.get('ANTHROPIC_API_KEY', 'NOT FOUND'))"

# 4. Run inference
python inference.py
```

If the key is still missing after step 2, set up Codespace Secrets (one-time fix).

---

*Source: claude_code_session_notes_full.md — live Codespace session. Keras/PyTorch with MNIST dataset.*
