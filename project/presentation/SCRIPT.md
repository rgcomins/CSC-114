# Predicting NC Housing Prices — Presentation Script (Ground Truth)

> **What this document is.** The single source of truth for the "science fair"
> presentation. Every slide is drafted here first — on-slide text, which visual
> to show, and the narration — so the HTML/JS slides can be built from a
> settled script instead of reverse-engineered from the code. If a number
> appears on a slide, it appears here first, traced to the run that produced it.
>
> **Tone.** Facetious science-fair energy (tri-fold poster, "The Big Question,"
> "The Envelope Please") wrapped around real, defensible ML work. The jokes are
> in the framing; the numbers are not jokes.
>
> **Sources.** `charter.md`, `sitreps/CHECKPOINT_Session_20260716.md` (the
> reconciled source of truth for the experiment series), the per-experiment
> SITREPs, both Sprint reflections, and `outputs/nc_housing_notes_v2.md`.
> Numbers are attributed to their run **timestamp** — see the Artifact Map
> (Appendix A) for the stamp → file correlation between `sitreps/` and
> `outputs/`.
>
> **Golden rule for the slide builder.** "Scaled" units × `TARGET_SCALE`
> (100,000) = dollars. All dollar figures below are already converted.

---

## Slide inventory (the poster at a glance)

| # | Section (poster panel) | Slide title | Visual |
|---|---|---|---|
| 1 | — | Predicting NC Housing Prices | title / hero |
| 2 | The Big Question | Can a machine price a neighborhood? | — |
| 3 | Background | We already did this once (the reskin) | CA→NC diagram |
| 4 | The Data | 5,637 NC block groups, some of them lying | data card |
| 5 | The Data | The cleaning saga (four bugs) | bug table |
| 6 | The Hypothesis | Drawing the finish line *before* we build | "good enough" card |
| 7 | Materials & Method | The model, the ruler, the referee | architecture card |
| 8 | Materials & Method | The One Change Rule (our lab discipline) | Sacred Flow strip |
| 9 | Results | Does it beat a coin flip? (baseline) | baseline bar |
| 10 | Results | When to stop: the turnaround epoch | `val_mae` curves |
| 11 | Results | Where it's right, where it's wrong | `pred_vs_actual` + `residuals` |
| 12 | Experiment 0 | One change: delete the impossible houses | `residuals_before_after` |
| 13 | The Main Event | One change: more folds (K=8 → K=4) | K comparison |
| 14 | The Main Event | One change: wider (64 → 128) | width comparison |
| 15 | The Main Event | One change: deeper (2 → 3 layers) | depth comparison |
| 16 | The Envelope Please | Nothing helped — and *that's* the finding | experiment scoreboard |
| 17 | The Diagnosis | Why bigger didn't win: MSE's long tail | MSE/RMSE table |
| 18 | Conclusion | The ceiling is the signal, not the size | conclusion card |
| 19 | Scope & Limits | What we deliberately did NOT do | scope-guard card |
| 20 | Future Work | The next level | roadmap |
| 21 | Reflection | What the process taught us | process card |
| 22 | — | Credits & artifacts | appendix / QR |

> Target length ~18–22 slides. Slides 13–15 are the heart of the talk (the
> user's requested focus: the one-change depth/width experiments). Slides 16–18
> are the payoff. Everything else is on-ramp and wind-down — cut here first if
> time is short.

---

# SLIDE 1 — Title

**ON SLIDE**
- **Predicting NC Housing Prices**
- *A neural network learns what a North Carolina neighborhood is worth*
- CSC-114 Artificial Intelligence I · Module 5–8 Mini-Project · Tabular cohort
- Solo project · [Your name] · 2026

**VISUAL:** Hero image — the `pred_vs_actual` scatter faded into the
background, or a stylized NC outline. Poster-board framing.

**NARRATION:**
"This is a science fair project. There's a board, there's a question, there's a
hypothesis we wrote down *before* we peeked at the answer, and there's a result.
The twist: our headline result is that the obvious idea — build a bigger model —
didn't work, and figuring out *why* is the whole story."

---

# SLIDE 2 — The Big Question

**ON SLIDE**
- **The question:** Given what the Census knows about a NC neighborhood —
  income, population, households, location, housing age — can we predict its
  **median home value**?
- One row = one census **block group** (~600–3,000 people).
- This is a **regression** problem: the answer is a dollar amount, not a
  yes/no.

**VISUAL:** A single example row rendered as a "trading card" (features on the
front, the price as the hidden answer).

**NARRATION:**
"We're not classifying cats vs. dogs. We're guessing a number — the typical
home value in a neighborhood — from eight-ish facts about that neighborhood.
It's the same problem the textbook does with California; we pointed it at
North Carolina instead."

---

# SLIDE 3 — Background: We already did this once

**ON SLIDE**
- Last module we trained a model on **California Housing** (1990 census).
- This project is a **reskin**: same shape, new data.
  - CA (1990, ~20,640 block groups) → **NC (2018, ~5,600 block groups)**
- Data: D. Michael Senter's `NC_Housing_Prices_2018.csv` — ACS 2018 5-year
  estimates + TIGER/Line centroids. Loads with one `pd.read_csv()`.
- Why this counts as real work: "same process, dataset I wasn't handed."

**VISUAL:** Side-by-side "before/after skin" diagram — California silhouette
with its 8 columns, arrow, North Carolina silhouette with the same columns.

**NARRATION:**
"The instructor literally blesses this path: take a process you already ran and
point it at a problem you chose. The muscle memory is the point. What's *new* is
that this dataset is real, recent, and — as we found out — a little bit broken."

---

# SLIDE 4 — The Data (and its lies)

**ON SLIDE**
- **Raw:** 5,637 rows × 9 columns. Target = `median_house_value` (dollars).
- **Features used (7):** `median_income`, `population`, `households`,
  `total_rooms`*, `housing_median_age`, `latitude`, `longitude`.
- *\*`total_rooms` is mislabeled — see next slide.*
- After cleaning: **5,635 rows** → train **4,508** / test **1,127**
  (80/20 split, seed 42).

**VISUAL:** Data card / mini schema table.

**NARRATION:**
"Six thousand neighborhoods, nine columns. Standard stuff — except several rows
are quietly wrong, and if you don't catch them they wreck the model. That's not
a bug in our project; that's the exercise."

---

# SLIDE 5 — The cleaning saga (four bugs)

**ON SLIDE** — table:

| # | The bug | What we did |
|---|---|---|
| 1 | `total_rooms` and `total_bedrooms` are **identical every row** (wrong ACS table pulled for both) | Kept one column; documented that its values are really bedroom counts. 7 features, not 8. |
| 2 | `9999` sentinel in `median_house_value` | Dropped those rows. |
| 3 | One row with `housing_median_age == 2018` (a bad "year built" leaked through) | In-script `!= 2018` filter. |
| 4 | **Two rows with age ≈ 2000** (impossible — 2,000-year-old houses) | Removed them. *This one mattered — Slide 12.* |

**VISUAL:** Four "wanted poster" mugshots for the four bad data patterns.

**NARRATION:**
"Four different flavors of bad data. Three are cosmetic. The fourth — houses
listed as two thousand years old — is the one that quietly poisoned our worst
predictions, and it's the first experiment we'll show you."

> **Ground-truth note for builder:** Bug #1 is why we report **7** features
> where California Housing has 8. Don't call the two columns independent.

---

# SLIDE 6 — The Hypothesis: draw the finish line first

**ON SLIDE**
- **Definition of "good enough" (written in the charter, before modeling):**
  1. Validation MAE **beats the naive baseline** (just predicting the average).
  2. Validation MAE **stops improving** — we can name the turnaround epoch.
- The metric is the **ruler** (MAE, in dollars). "Good enough" is the **line we
  draw on it**. A project needs both.

**VISUAL:** A ruler graphic with a line drawn on it labeled "good enough."

**NARRATION:**
"The boss fight of this module isn't code — it's deciding what 'done' means
*before* you start, so you don't polish forever. We committed to two measurable
signals in writing. Both were falsifiable. Spoiler: we hit both."

---

# SLIDE 7 — Materials & Method: model, ruler, referee

**ON SLIDE**
- **Model:** feed-forward neural net, **2 hidden layers × 64 units**, ReLU,
  single linear output. Keras 3 on the PyTorch backend.
- **Ruler (metric):** **MAE** — mean absolute error, in dollars. "On average,
  how many dollars are we off?"
- **Referee (validation):** **k-fold cross-validation** — train on k−1 slices,
  test on the held-out slice, rotate, average. Honest error, not lucky-split
  error.
- Trained 50 epochs; a separate **held-out test set** (never in any fold) is
  the final exam.

**VISUAL:** Three-panel card: [network diagram] · [MAE formula in plain words]
· [k-fold rotation strip].

**NARRATION:**
"Small model on purpose — the textbook's Housing architecture. MAE is our ruler
because it's in dollars and a human can feel it. K-fold is our referee so we're
not fooling ourselves with one lucky train/test split."

---

# SLIDE 8 — The One Change Rule (our lab discipline)

**ON SLIDE**
- Every experiment changed **exactly one thing**, then re-ran the whole
  pipeline.
- Everything else held fixed: same data, same split seed, same weight-init
  seed, same 50 epochs.
- Workflow: **Issue → Branch → PR → Review → Merge** (never commit to main).
- Every run writes a **timestamped** bundle (log + plots) — nothing overwrites
  anything, so every claim is reproducible from its stamp.

**VISUAL:** Sacred Flow arrow strip + a "1 knob turned per run" dial graphic.

**NARRATION:**
"This is the part that makes the results trustworthy. If you change three things
and the number moves, you've learned nothing. We changed one knob at a time — K,
then width, then depth — held the seeds fixed, and stamped every run. That
discipline is why the boring result on the next slides is actually a *result*
and not just noise."

> **Builder note:** This slide sets up 13–15. The audience must leave it
> understanding "one variable per experiment." It's the thesis of the whole
> middle act.

---

# SLIDE 9 — Result 1: Does it beat a coin flip?

**ON SLIDE**
- **Naive baseline** (predict the mean for everyone): **~$78,878** MAE (CV),
  ~$77,808 on the test set.
- **Our model:** **~$41,407** MAE (CV, k=8), **~$43,466** on the test set.
- **≈47% lower error than guessing the average.** ✅ Criterion 1 met.

**VISUAL:** Two-bar comparison — tall grey "guess the average" bar (~$78.9K)
vs. short blue "our model" bar (~$41.4K). Big "−47%" callout.

**NARRATION:**
"First checkpoint from the charter: beat the dumb baseline. Guessing the
statewide average is off by about seventy-nine thousand dollars per
neighborhood. Our model is off by about forty-one. That's roughly half the
error — the model is genuinely learning something."

> **Builder note:** Baseline numbers from `charter.md` (k=8, measured 07-15).
> Keep baseline and model on the *same* validation basis when you draw the bars.

---

# SLIDE 10 — Result 2: When to stop (the turnaround epoch)

**ON SLIDE**
- Criterion 2: validation MAE **stops improving** — where?
- It drops fast, then **flattens around epoch ~12–13**.
- After that it just **oscillates** in a noisy ~0.403–0.427 band (global min
  near epoch 22 is within the noise). ✅ Criterion 2 met.
- Lesson from Module 4: the canned script trains *past* this point. More epochs
  ≠ better.

**VISUAL:** `graphs/nc_housing_val_mae.png` (full curve) with the truncated
version `graphs/nc_housing_val_mae_truncated.png` as an inset. Mark epoch ~12–13.

**NARRATION:**
"The curve nose-dives for a dozen epochs, then goes flat and starts jittering.
That flat-and-jittery zone is the model saying 'I've learned what I can.' Naming
that turnaround epoch was our second finish-line criterion. The zoomed-in
version on the right shows there's no hidden improvement after epoch 13 — just
noise."

---

# SLIDE 11 — Where it's right, where it's wrong

**ON SLIDE**
- **Predicted vs. actual:** points hug the "perfect prediction" line for
  ordinary neighborhoods…
- …but the model **under-predicts** the rare, very expensive block groups
  (points fall below the line on the right).
- **Residuals** are a tight spike near \$0 with a **long right tail** — a few
  big misses, not broad sloppiness.

**VISUAL:** Left: `graphs/nc_housing_pred_vs_actual.png` (with the red perfect-
prediction line). Right: `graphs/nc_housing_residuals.png`.

**NARRATION:**
"Two diagnostic plots. On the left, most neighborhoods sit right on the diagonal
— good. But look at the expensive homes on the right: the model consistently
guesses too low. On the right plot, the errors pile up near zero with a tail
stretching out — meaning most guesses are close and a handful are way off. Hold
that thought; it becomes the diagnosis at the end."

---

# SLIDE 12 — Experiment 0: delete the impossible houses

**ON SLIDE**
- **The one change:** remove the two rows with age ≈ 2000. Nothing else.
- Controlled A/B (`before_after_residuals.py`): same source, same seeds, same
  architecture, same 50 epochs — only the two rows toggled.

| Metric | BEFORE (kept) | AFTER (removed) |
|---|---|---|
| Test MAE | \$54,370 | **\$44,522 (~18% lower)** |
| Worst single error | **\$6,772,774** | \$593,503 |
| Rows | 5,637 | 5,635 |

**VISUAL:** `graphs/nc_housing_residuals_before_after.png` (the two-panel red
"before" / green "after" histogram). The before panel's tail out to \$6.7M is
the punchline.

**NARRATION:**
"First application of the One Change Rule, and a clean win. Two impossible rows
were producing multi-million-dollar predictions against sub-\$400K homes.
Delete just those two rows — change nothing else — and the worst error collapses
from \$6.8 million to under \$600K, and test error drops ~18%. Honest caveat: the
*k-fold average* barely moved, because the damage was concentrated in a few
catastrophic test predictions, not spread across the average. Good data beats a
bigger model — which foreshadows everything next."

---

# SLIDE 13 — Main Event, Change #1: more folds (K=8 → K=4)

**ON SLIDE**
- **The one change:** cross-validation folds 8 → 4. Model untouched.
- Run `110751` (K=8) vs. `114435` (K=4).

| | K=8 (baseline) | K=4 |
|---|---|---|
| CV MAE | 0.418 → \$41,762 | 0.415 → \$41,451 |
| Test MAE | 0.429 → \$42,870 | 0.422 → \$42,165 |

- Difference: ~\$300 CV, ~\$700 test — **noise**.
- **Takeaway:** K is a knob on the *validation procedure*, not the model.

**VISUAL:** Small paired-bar or slope chart, K=8 vs K=4. Label "changed: folds."

**NARRATION:**
"First knob: how many folds we validate with. Going from 8 to 4 moved the number
by a few hundred dollars — well inside the fold-to-fold noise. That's the
correct result: K changes how carefully we *measure*, not how good the model
*is*. A good sanity check that our harness behaves."

---

# SLIDE 14 — Main Event, Change #2: wider (64 → 128)

**ON SLIDE**
- **The one change:** hidden layers 2×**64** → 2×**128**. Twice the width.
- Run `114435` (width 64) vs. `115653` (width 128).

| | 2×64 | 2×128 |
|---|---|---|
| CV MAE | 0.415 → \$41,451 | 0.418 → \$41,786 |
| Test MAE | 0.422 → \$42,165 | 0.434 → \$43,409 |

- Wider was **flat-to-slightly-worse**. More parameters did **not** help.

**VISUAL:** Paired bars, 2×64 vs 2×128. Label "changed: width." A ghosted
"bigger brain" icon with a red ✗.

**NARRATION:**
"Second knob: make each layer twice as wide — more neurons, more capacity. The
intuition is 'bigger model, better fit.' It didn't happen. Wider was flat, even
a touch worse on the test set. First real hint that our problem isn't a
capacity problem."

---

# SLIDE 15 — Main Event, Change #3: deeper (2 → 3 layers)

**ON SLIDE**
- **The one change:** add a third hidden layer. 2×64 → **3×64**.
- Run `114435` (2 layers) vs. `120939` (3 layers).

| | 2×64 | 3×64 |
|---|---|---|
| CV MAE | 0.415 → \$41,451 | 0.430 → \$42,991 |
| Test MAE | 0.422 → \$42,165 | 0.430 → \$42,999 |

- Deeper was **slightly worse** on both.

**VISUAL:** Paired bars, 2×64 vs 3×64. Label "changed: depth." Network diagram
gaining a layer, red ✗.

**NARRATION:**
"Third knob: make the network deeper — another layer to learn more abstract
combinations. Also didn't help; if anything, it hurt. Two independent ways of
adding capacity — wider *and* deeper — both refused to improve. When two
different bigger-hammer attempts both miss, the wall isn't the hammer."

---

# SLIDE 16 — The Envelope, Please: nothing helped

**ON SLIDE** — the scoreboard:

| Run | Config | Changed | CV MAE | Test MAE |
|---|---|---|---|---|
| `110751` | 2×64, K=8 | baseline | \$41,762 | \$42,870 |
| `114435` | 2×64, K=4 | folds | \$41,451 | \$42,165 |
| `115653` | 2×128, K=4 | **width** | \$41,786 | \$43,409 |
| `120939` | 3×64, K=4 | **depth** | \$42,991 | \$42,999 |
| `123043` | 2×64, K=4 | +MSE report | \$41,375 | \$42,123 |

- Every per-fold score stayed in the **~0.40–0.46 band**. All differences are
  within noise.
- **The finding:** the model is **not capacity-limited.** More width, more
  depth → no gain.

**VISUAL:** All five runs as a dot/bar strip on one axis, with a shaded "noise
band" behind them showing they all overlap. The "aha": the bars are all the
same height.

**NARRATION:**
"Here's the envelope. Five runs, one knob each. Line them up and they're all the
same height — every score lands in the same narrow band. In a science fair
you're trained to want the bar that shoots up. We don't have one. And that
*negative* result is the actual discovery: you cannot make this model better by
making it bigger. So the next question is the interesting one — *why not?*"

> **Builder note:** This is the emotional peak. Design the 'all bars equal'
> visual so the flatness is obvious and intentional, not like missing data.

---

# SLIDE 17 — The Diagnosis: MSE's long tail

**ON SLIDE**
- We added MSE/RMSE reporting (run `123043`) to see *why*.

| Metric | Cross-val (K=4) | Held-out test |
|---|---|---|
| MAE | 0.414 → \$41,375 | 0.421 → \$42,123 |
| RMSE | 0.650 → \$64,988 | 0.656 → \$65,576 |
| **RMSE − MAE gap** | 0.236 | 0.235 |

- **RMSE ≈ 1.6× MAE**, stably. RMSE squares errors first → a **few big misses**
  dominate.
- **Tail compression:** the worst block group (~\$1.04M actual) was predicted
  ~\$427K (2×64) → ~\$400K (2×128) → ~\$393K (3×64). Adding capacity pushed the
  expensive-home guesses *lower*, not closer.

**VISUAL:** The `pred_vs_actual` scatter again with the under-predicted
high-value points circled, beside the MAE-vs-RMSE gap as a small bar pair.

**NARRATION:**
"To diagnose, we reported RMSE alongside MAE. RMSE is consistently about 1.6
times MAE — and because RMSE squares errors, that gap is the fingerprint of a
few large misses, not uniform sloppiness. Those misses are the rare expensive
neighborhoods. And here's the kicker: every time we added capacity, the model
guessed those expensive homes *even lower*. An MSE-trained model plays it safe
on rare high-value cases, and a bigger model plays it safer. The ceiling is
built into the loss function and the signal — not the model size."

---

# SLIDE 18 — Conclusion: the ceiling is the signal, not the size

**ON SLIDE**
- ✅ **Beat the baseline** (~47% lower error than guessing the mean).
- ✅ **Found the turnaround epoch** (~12–13).
- **Headline:** the model is **not capacity-limited.** Width and depth both
  failed to help.
- **Why:** the error ceiling is set by (a) how much signal is in 7 features and
  (b) MSE's tail compression on rare expensive homes — **not** by model size.
- Both charter criteria met; the honest verdict is "good enough, and we know
  exactly what's holding it back."

**VISUAL:** Clean conclusion card. A "ceiling" line the bars can't break
through, labeled "signal + loss behavior, not model size."

**NARRATION:**
"So: we met both goals we wrote down in advance, and we can explain the wall we
hit. Making the model bigger is the wrong lever. If we wanted to do better,
we'd change the *signal* — more or better features — or the *loss* — stop
punishing the model in a way that makes it flinch from expensive homes. That's a
much more useful conclusion than 'we added layers and the number went down.'"

---

# SLIDE 19 — Scope: what we deliberately did NOT do

**ON SLIDE**
- ❌ Not building a general ACS cleaning pipeline — only fixed *this* file's
  known bad rows.
- ❌ Not re-deriving features from the raw Census API — used the pre-built CSV.
- ❌ No deployment, no UI — model + evaluation only.
- Why it matters: the "What we are NOT doing" line is what kept a solo,
  four-week project finishable.

**VISUAL:** Scope-guard card — three struck-through temptations.

**NARRATION:**
"A science fair board should say what it *isn't*. Over-scoping is the number-one
way these projects die. We wrote the guardrails into the charter on day one and
held the line: fix this file, use this CSV, no app. That's why there's a finished
project to present."

---

# SLIDE 20 — Future Work: the next level

**ON SLIDE**
- **Signal, not size:** engineer features (e.g. rooms-per-household), or pull
  fresh 2020–2024 ACS data from the Census API.
- **Fix the flinch:** try a loss less brutal on the tail (e.g. Huber, or log-
  transform the target) so expensive homes aren't systematically under-guessed.
- **Stop earlier:** read the turnaround off the sharper MSE curve and train
  fewer epochs.
- **The known limit:** rare high-value neighborhoods remain hard — that's a
  data-coverage problem, not a tuning problem.

**VISUAL:** Roadmap arrow with three forks (features / loss / early-stop).

**NARRATION:**
"If there were a Module 9, this is where we'd go — and notice none of it is
'add more layers.' The experiments told us to stop tuning size and start
changing the signal and the loss. That's the payoff of doing the boring
experiments honestly: they point you at the *right* next move."

---

# SLIDE 21 — Reflection: what the process taught us

**ON SLIDE**
- The **One Change Rule** turned a flat result into a *trustworthy* result.
- Timestamped runs meant every claim on this poster is reproducible from a
  stamp.
- The biggest single win was **data cleaning**, not modeling (Slide 12).
- "Define good enough first" stopped us from chasing a bigger model forever.

**VISUAL:** Process card — Sacred Flow + "1 change / run" + "stamp everything."

**NARRATION:**
"The real lesson wasn't about neural networks. It was that disciplined
process — one change per experiment, everything stamped, the finish line drawn
first — is what let us confidently say 'bigger won't help.' Without that
discipline, five nearly-identical numbers would've looked like failure instead
of a finding."

---

# SLIDE 22 — Credits & Artifacts

**ON SLIDE**
- **Data:** D. Michael Senter, `NC_Housing_Prices_2018.csv` (ACS 2018 5-yr +
  TIGER/Line). Public-domain source.
- **Stack:** Python · pandas · Keras 3 (PyTorch backend) · matplotlib · GitHub
  Codespaces · Sacred Flow.
- **Reproduce it:** `run.sh` → `nc_housing_model_v2.py`. Every run's log +
  plots live in `outputs/` under a shared timestamp.
- Course: CSC-114 · Tabular cohort · Modules 5–8 mini-project.

**VISUAL:** Appendix card / optional QR to the repo. Small thumbnail strip of
all five graphs.

**NARRATION:**
"Everything's reproducible. One script, one command, and every figure on this
board traces back to a timestamped run in the outputs folder. Thanks for
visiting the booth."

---

# Appendix A — Artifact Map (stamp → files)

Correlates `sitreps/` (the write-ups) with `outputs/` (the logs + graphs).
Every artifact from a run shares one timestamp; no run overwrites another.

| Experiment | Stamp | Config | SITREP(s) | Graphs (in `outputs/`) |
|---|---|---|---|---|
| Baseline | `20260716_110751` | 2×64, K=8, full | `SITREP_v2_Baseline_Confirmation` | `nc_housing_{val_mae,val_mae_truncated,pred_vs_actual,residuals}_20260716_110751.png` |
| K sweep | `20260716_114435` | 2×64, **K=4** | `SITREP_K4_Fold_Experiment`, `Comparison_K8_vs_K4` | …`_20260716_114435.png` |
| Width | `20260716_115653` | **2×128**, K=4 | `SITREP_Width_Experiment`, `Comparison_Width64_vs_Width128` | …`_20260716_115653.png` |
| Depth | `20260716_120939` | **3×64**, K=4 | `SITREP_Depth_Experiment` | …`_20260716_120939.png` |
| MSE capture | `20260716_123043` | 2×64, K=4, +MSE/RMSE | `SITREP_MSE_RMSE_Validation` | …`_20260716_123043.png` + `nc_housing_val_mse[_truncated]_20260716_123043.png` |
| (Cross-run) | — | 2×64 vs 2×128 vs 3×64 | `Comparison_Architecture_Experiments` | — |

**Canonical "clean" graphs for slides** (untimestamped, in `graphs/`) — use
these on the slides, cite the stamped originals in the appendix:
`nc_housing_val_mae.png`, `nc_housing_val_mae_truncated.png`,
`nc_housing_pred_vs_actual.png`, `nc_housing_residuals.png`,
`nc_housing_residuals_before_after.png`.

The overview reconciliation of the whole series lives in
`sitreps/CHECKPOINT_Session_20260716.md` — treat it as the tiebreaker if any two
documents disagree on a number.

---

# Appendix B — Number provenance (so no slide invents a figure)

- **Naive baseline** \$78,878 CV / \$77,808 test — `charter.md` (k=8, 07-15).
- **Final charter model** \$41,407 CV / \$43,466 test — `charter.md` (k=8, 07-15).
  *(Slides 9–10 use these charter numbers.)*
- **Experiment series** (Slides 13–17) — `CHECKPOINT` PART 2 table, runs
  `110751`–`123043`. These are the k=4 series; do not mix them with the k=8
  charter numbers on the same axis.
- **Age-2000 A/B** \$54,370 → \$44,522, worst \$6,772,774 → \$593,503 —
  `before_after_residuals.py`, reported in `Sprint 2 Reflection.md`.
- **MSE/RMSE** table — `CHECKPOINT` PART 2, run `123043`.
- **Tail compression** \$427K → \$400K → \$393K on the ~\$1.04M block —
  `CHECKPOINT` PART 3, finding 4.

> If a future run changes any of these, update the number *here first*, then in
> the slide. This appendix is the contract.
