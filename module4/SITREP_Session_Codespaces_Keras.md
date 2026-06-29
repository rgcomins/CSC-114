# SITREP — CSC 114 Lab Session
**Classification:** UNCLASSIFIED // FOR ACADEMIC USE**
**DTG:** 24 JUN 2026
**Subject:** Codespaces / Claude Code / Keras+PyTorch Inference Pipeline
**Prepared for:** Rick (CSC 114, Section 1001)

---

## BLUF
Environment stood up, API connected, MNIST model trained and executing inference. Two critical failure modes identified and resolved: API key persistence failure (environment reload) and segfault from conflicting backends (TF vs. PyTorch). Mission complete. System operational.

---

## SITUATION

Working environment: GitHub Codespace (cloud-hosted Linux VM).
Objective: Establish a functional Keras/PyTorch deep learning pipeline from scratch — install tooling, connect to Anthropic API, train an MNIST classifier, and run live inference on test images.

---

## TASKS COMPLETED

| # | Task | Outcome |
|---|---|---|
| 1 | Install Claude Code | Complete — native installer used (no Node.js dependency) |
| 2 | Verify API key in bash environment | Complete — confirmed correct `export` syntax |
| 3 | Test Anthropic API connectivity | Complete — client instantiated, response confirmed |
| 4 | Diagnose API key loss after VS Code reload | Complete — root cause identified (window reload killed terminal), fix applied via `~/.bashrc` and Codespace Secrets |
| 5 | Build and understand Sequential Keras model | Complete — Dense(512, relu) + Dense(10, softmax) architecture understood and implemented |
| 6 | Understand epoch/early stopping tradeoffs | Complete — learning curve analysis method confirmed |
| 7 | Diagnose and fix TF/PyTorch segfault on inference | Complete — root cause: dual-backend initialization; fix: standalone `import keras` with `KERAS_BACKEND=torch` |
| 8 | Execute final inference script | Complete — model loads, predicts, outputs labeled image to file |

---

## INCIDENTS / FRICTION ENCOUNTERED

**Incident 1 — API Key Loss**
Trigger: VS Code Python extension install triggered a full window reload, killing all terminal sessions and wiping exported variables.
Resolution: API key written to `~/.bashrc` for session persistence; long-term fix via GitHub Codespace Secrets (survives all reloads and restarts).

**Incident 2 — Segfault on Inference**
Trigger: Inference script used `from tensorflow import keras` while model was trained with Keras/PyTorch backend — caused both TF and PyTorch to initialize simultaneously.
Resolution: Replaced with standalone `import keras` after setting `os.environ["KERAS_BACKEND"] = "torch"` *before* any keras import. Backend conflict eliminated.

---

## CURRENT STATUS

- Environment: Stable
- Model: Trained and saved (`mnist_best_model.keras`)
- Inference: Operational — accepts test index, outputs prediction + labeled image file
- API integration: Confirmed working

---

## NEXT ACTIONS

| Priority | Action | Due |
|---|---|---|
| HIGH | Complete Steps 3–4 of Apply AI Frameworks (fit + save/predict) | 6/21/26 |
| HIGH | Submit reflection document for Apply AI Frameworks | 6/21/26 |
| MEDIUM | Begin Apply/Assess Classification & Regression | 6/28/26 |
| LOW | Continue YAML course assistant agent refinement | Ongoing |

---

*Source: claude_code_session_notes_full.md — live Codespace session record.*
