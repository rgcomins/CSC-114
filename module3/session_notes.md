# Session Notes: Codespaces, Claude Code & Keras

---

## 1. Installing Claude Code

Two options:

**Native installer (recommended — no Node.js required):**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**npm (use if you need version pinning):**
```bash
npm install -g @anthropic-ai/claude-code
```

> ⚠️ Never use `sudo` with the npm install — it causes permission issues. If you hit permission errors, configure npm to use a user-owned directory instead.

Verify the install:
```bash
claude --version
```

Requires a Claude Pro, Max, Teams, Enterprise, or Console (API) account. The free plan does not include Claude Code.

---

## 2. Checking Environment Variables in Bash

```bash
echo $VARIABLE_NAME
```

Safer forms:
```bash
echo "$MY_VAR"           # preserves whitespace
declare -p MY_VAR        # shows type + value
```

Always quote your variable references (`"$VAR"`) to handle values with spaces or special characters.

---

## 3. Testing the Anthropic API Connection

```python
import anthropic

client = anthropic.Anthropic()  # automatically uses ANTHROPIC_API_KEY

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=32,
    messages=[{"role": "user", "content": "Say 'API connection successful!'"}]
)

print(response.content[0].text)
```

Run with:
```bash
python test_connection.py
```

---

## 4. Fix: API Key Not Found in Codespace

### The error
```
TypeError: Could not resolve authentication method. Expected one of api_key, auth_token,
or credentials to be set.
```

### Why it happened
The VS Code **Python extension was installed mid-session**, which triggered a **window reload**. This killed all terminal sessions — wiping any `export`ed variables in the process.

### Diagnostic
```bash
echo $ANTHROPIC_API_KEY                                  # check in shell
python -c "import os; print(os.environ.get('ANTHROPIC_API_KEY', 'NOT FOUND'))"  # check in Python
```

If `echo` shows the key but Python prints `NOT FOUND`, the variable isn't being inherited by child processes.

### Fix 1 — Persist in `~/.bashrc` (survives reloads)
```bash
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

For zsh (check with `echo $SHELL`):
```bash
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### Fix 2 — Pass inline for a one-off run
```bash
ANTHROPIC_API_KEY="your-key-here" python test_connection.py
```

### Fix 3 — GitHub Codespace Secrets (best long-term solution)
`GitHub → Settings → Codespaces → New secret → ANTHROPIC_API_KEY`

Secrets are automatically available as environment variables in every session and survive restarts.

### Common cause: forgetting `export`
```bash
ANTHROPIC_API_KEY="sk-..."   # ❌ local only — child processes can't see it
export ANTHROPIC_API_KEY="sk-..."  # ✅ inherited by child processes
```

> ⚠️ Never paste your API key in plain text in a chat or shared document. Revoke and regenerate it immediately if this happens at [console.anthropic.com](https://console.anthropic.com).

---

## 5. Using Claude Code in a Codespace

Open an interactive session:
```bash
claude
```

One-off commands:
```bash
claude "explain what this codebase does"
claude "fix the bug in test_connection.py"
claude "add error handling to my script"
```

Useful flags:
```bash
claude --help       # all options
claude --version    # check version
claude -p "prompt"  # non-interactive, prints response and exits
```

---

## 6. Keras Model — Understanding the Layers

```python
model = keras.Sequential([
    layers.Dense(512, activation="relu"),
    layers.Dense(10, activation="softmax"),
])
```

### First layer: `Dense(512, activation="relu")`
- 512 neurons that learn features from the input data
- `relu` (Rectified Linear Unit) is standard for hidden layers — it learns non-linear patterns without outputting probabilities

### Last layer: `Dense(10, activation="softmax")`
- 10 neurons — one per class (e.g. digits 0–9 for MNIST)
- `softmax` converts the 10 raw scores into **probabilities that sum to 1.0**

Example output:
```
[0.02, 0.01, 0.01, 0.03, 0.01, 0.02, 0.01, 0.85, 0.02, 0.02]
```
This means the model is 85% confident the input is a **7** (index 7).

Get the predicted class:
```python
prediction = model.predict(x)
predicted_class = prediction.argmax()  # → 7
```

`softmax` is the standard choice for multi-class classification and works well with `categorical_crossentropy` loss.

---

## 7. Epoch Behavior: All Epochs vs. Early Stopping

### Default — always runs all epochs
```python
model.fit(x_train, y_train, epochs=50)  # always runs all 50
```

### Early stopping — halts when improvement stalls
```python
from tensorflow.keras.callbacks import EarlyStopping

early_stop = EarlyStopping(
    monitor="val_loss",        # metric to watch
    patience=5,                # stop after 5 epochs with no improvement
    restore_best_weights=True  # roll back to the best epoch
)

model.fit(x_train, y_train,
          epochs=50,
          validation_data=(x_val, y_val),
          callbacks=[early_stop])
```

| Parameter | What it does |
|---|---|
| `monitor` | Metric to watch (`"val_loss"`, `"val_accuracy"`, etc.) |
| `patience` | How many bad epochs to tolerate before stopping |
| `restore_best_weights` | Rolls back to the best checkpoint (almost always use `True`) |
| `min_delta` | Minimum change that counts as "improvement" |

---

## 8. How to Choose the Number of Epochs

### 1. Early stopping (most practical)
Set `epochs` generously high and let early stopping find the natural stopping point.

### 2. Plot the learning curves
```python
history = model.fit(...)

import matplotlib.pyplot as plt
plt.plot(history.history["loss"], label="train loss")
plt.plot(history.history["val_loss"], label="val loss")
plt.legend()
plt.show()
```

### 3. Rules of thumb by dataset size

| Dataset size | Starting point |
|---|---|
| Small (<10k samples) | 50–100 epochs |
| Medium | 20–50 epochs |
| Large | 10–20 epochs |

### 4. Trial run
Train once with early stopping, note where it stopped, use that number (plus a small buffer) for future runs.

The recommended workflow is **early stopping + learning curve plotting** together.

---

## 9. Reading a Learning Curve

The learning curve plots **training loss** and **validation loss** over epochs.

**What to look for:**

| Zone | What's happening |
|---|---|
| Both losses falling | Model is genuinely learning — good |
| Val loss flattens | Model has learned what it can — sweet spot |
| Train loss keeps falling, val loss rises | **Overfitting** — model is memorizing training data |

The **sweet spot** is the epoch where validation loss is at its lowest before it starts rising again. Early stopping targets this point automatically using `patience`.

The wider the gap between training loss and validation loss in the overfitting zone, the more overfit the model is.

---

*Notes generated from a live Codespace session covering environment setup, API integration, and intro Keras concepts.*
