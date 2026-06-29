# Module 4 — Apply: Build a Chapter 4 Model With Your Agent

**CSC-114 Artificial Intelligence I**
**Type:** Apply (graded on a successful work session, not on perfect code)

---

## The goal

Pick one of the two examples from Chapter 4 and build a working version of it **together with your class AI assistant**. By the end you should have code that runs, trains, and produces sensible output — plus a saved picture of your own training curve.

This is an **Apply** task. You are not being graded on getting a "right" answer. You're being graded on **whether you had a real, productive work session with your agent and ended up with something that works.**

---

## Step 1 — Choose your example

Pick **one**:

- **Option A — Movie reviews (Classification).** Predict whether an IMDB review is positive or negative. Reference: `ground_truth_imdb.md`.
- **Option B — House prices (Regression).** Predict the median home price of a California district. Reference: `ground_truth_california_housing.md`.

> The Reuters "pick 1 of 46 topics" example from the chapter is fine to read, but it's more complex than we need right now — we'll come back to multiclass later. Stick to A or B.

Open the matching **ground truth** doc before you start and skim it. It's your map. Keep it open while you work so you can check your agent against it.

---

## Step 2 — (Optional, recommended) Make it yours

A model you tweaked is more interesting to reflect on than one you copied. Try one small change:

- **Option A ideas:** filter to a subset of reviews, change `num_words`, or change the layer sizes.
- **Option B ideas:** drop or add a feature, change the number of K-folds, or change the layer sizes.
- **Either:** find a *different but similar* public dataset and ask your agent how you'd adapt the code.

Keep it to **one change** so you can actually tell what it did (the one-change rule).

---

## Step 3 — Build it with your agent

Work in a **GitHub Codespace** using your class AI code assistant (setup covered in class). The work itself is a conversation: you ask, the agent drafts, you run it, you read the output, you push back when something looks off.

A good session usually moves through: load the data → prepare it (encode/normalize/scale) → build the model → compile → train with a validation check → plot the training curve → evaluate → predict on a sample.

**You're "done" when:**

1. The code **runs end to end without errors.**
2. The model **trains** and the loss goes **down** over epochs.
3. You produced a **training-vs-validation curve** and **saved it** (screenshot or image file).
4. You can point to the **epoch where validation stops improving** — the overfitting turnaround. (You'll need this for the Assess task, so don't skip it.)

---

## Step 4 — Submit (by track)

**Code Builders**

- Do the work on a branch and open a PR following the Sacred Flow (Issue → Branch → PR → Review → Merge).
- Your PR should include: the notebook or script, the saved training curve, and a short README note saying which option you picked and what one change (if any) you made.

**Prompt Masters**

- Run the example with your agent and drive the changes through conversation.
- Submit: a screenshot (or short screen capture) showing the code running and the final output, **plus** your saved training curve, **plus** a one-paragraph note on which option you picked and what one change you made.
- Drag-and-drop into the assignment, or paste your screenshots — whatever the class drop method is.

---

## What "good" looks like here

You don't need 95% accuracy or a tiny MAE. You need evidence of a **real working session**: code that runs, a model that learns, a curve you can read, and a couple of moments where you noticed something and steered the agent. Messy is fine. Stuck-and-then-unstuck is great — that's the work.

```
INSTRUCTOR APPENDIX — remove before posting to students if you want a clean copy

GRADING (light / completion-based)
This Apply is pass-style. Confirm the four "done" criteria:
  [ ] Code runs end to end.
  [ ] Loss decreases over epochs (model is actually learning).
  [ ] A training/validation curve was produced AND saved.
  [ ] Student can name their overfitting turnaround epoch.
Award full credit for a genuine working session even if the model is mediocre.
The rubric-graded thinking happens in the Assess task, not here.

THE ANCHOR
Step 3 criterion #4 (saved curve + named turnaround epoch) is the hook that
makes the Assess task copy-proof. A student who skipped the real run cannot
answer the Assess questions in their own words about their own numbers. If a
submission has no saved curve, send it back before they start Assess.

EXPECTED TURNAROUND (for your reference)
  Option A (IMDB):    validation peaks ~epoch 4.
  Option B (Housing): validation MAE flattens ~120–140 epochs.
Students who tweaked layer sizes / num_words / features will see different
numbers — that's fine and actually better for reflection.

TRACK NOTES
  Code Builders submit via Sacred Flow PR (branch from a Module 4 issue).
  Prompt Masters submit screenshots/capture + saved curve + one-paragraph note.
  Both must include the saved curve — it's the shared anchor.

FAST-MOVING TARGETS (re-verify each term)
  - Keras 3 with the JAX backend is the assumed stack; confirm install line
    and backend env var in your class Codespace setup doc.
  - Codespaces UI, AI code-assistant login path, and free-tier limits drift.
    Verify the live setup steps before the module opens.
  - Dataset download sizes/URLs (IMDB ~80MB; California Housing small) can
    change with Keras versions.
  - Reconcile any older handout that says "Google Colab" with the
    Codespaces-only framing used here.
```

---

*Built against Chapter 4 of Chollet & Watson, "Deep Learning with Python," 3rd Edition (deeplearningwithpython.io). Pair this with `ground_truth_imdb.md` or `ground_truth_california_housing.md`.*
