# CHECKPOINT — CSC 114 Lab Session

**Classification:** UNCLASSIFIED // FOR ACADEMIC USE
**DTG:** 16 JUL 2026
**Subject:** `nc_housing_model_v2.py` — environment bring-up, bug fixes, and 5-run experiment series
**Purpose:** Single consolidated record of everything done this session, so all
independently-written per-run SITREPs reconcile against one source of truth.
**Script under test:** `project/nc_housing_model_v2.py`
**Data:** `project/NC_Housing_Prices_ready.csv`

---

## BLUF

Brought the v2 pipeline up from a cold, dependency-less environment; fixed one
real runtime bug and three manual-edit syntax/logic errors; then ran a clean
five-run experiment series (baseline → K sweep → width → depth → MSE capture).

**Headline finding:** the model is **not capacity-limited.** Neither more width
(64→128) nor more depth (2→3 layers) improved accuracy; both were flat-to-worse.
Adding MSE/RMSE reporting quantified *why*: RMSE (~$65K) is ~1.6× MAE (~$42K), a
stable gap driven by a handful of large misses on high-value block groups — a
tail-compression property of MSE-trained regression, not a capacity shortfall.

---

## PART 1 — Environment bring-up & fixes (blockers cleared)

| # | Symptom | Root cause | Fix |
|---|---|---|---|
| 1 | `ModuleNotFoundError: numpy` | No Python deps installed | `pip install numpy pandas matplotlib keras tensorflow` |
| 2 | `ModuleNotFoundError: torch` at keras import | Script pins `KERAS_BACKEND=torch`; torch absent | `pip install torch` |
| 3 | `FileNotFoundError: project/NC_Housing_Prices_ready.csv` | Default `--data` path assumes repo root; we `cd`'d into `project/` | Pass `--data NC_Housing_Prices_ready.csv` (local path) |
| 4 | Crash at `model.evaluate()` **after** training: `'_Tee' object has no attribute 'encoding'` | `_Tee` stdout/log fan-out didn't expose `encoding`; Keras's progress bar queries `sys.stdout.encoding` | **Code fix:** added `__getattr__` to `_Tee` delegating unknown attrs (`encoding`, `isatty`, `fileno`, …) to the real console stream |

> Fix #4 is a genuine script bug, not just environment setup — without it, *every*
> run would crash at the evaluate step after training completed. This is the item
> most likely to be missing from a per-run SITREP that only saw the final green run.

**Manual-edit errors caught and corrected during the session:**

| Where | Broken edit | Correction |
|---|---|---|
| `KEEP_COLS` | Renamed feature to `total_bedrooms` → `usecols` mismatch (CSV header is literally `total_rooms`) | Reverted to `total_rooms`; comment now states the values are really bedroom counts |
| `k` (fold count) | `k = 4 // 7/16 - changed to 4fold` → `//` is floor-division, `4fold` an invalid literal | `k = 4  # 7/16 - changed from 8-fold to 4-fold` |
| Model layer 2 (width run) | `Dense(128 activation="relu")` → missing comma | `Dense(128, activation="relu")` |

**Data-semantics note (closed):** The `ready` CSV contains only `total_rooms`.
The raw source `not_cleaned/NC_Housing_Prices_2018.csv` carries both
`total_bedrooms` and `total_rooms` — **verified identical in 2000/2000 rows**, a
duplicate-column artifact in the source. Decision: keep the header name
`total_rooms`, document that its values mean total_bedrooms. No numeric impact.

---

## PART 2 — Experiment series

All runs: full mode (50 epochs), torch backend, 80/20 split (seed 42),
5,635 rows after cleaning (train 4,508 / test 1,127), features = 7.
"Scaled" units × `TARGET_SCALE` (100,000) = dollars.

| Run | Stamp | Config | CV MAE | Test MAE | Notes |
|---|---|---|---|---|---|
| Smoke test | `105549` | `--quick`, 2×64, K=8 | 0.418 → $41,784 | 0.419 → $41,887 | first green run (post `_Tee` fix) |
| Baseline | `110751` | full, 2×64, **K=8** | 0.418 → $41,762 | 0.429 → $42,870 | v1-parity baseline |
| K sweep | `114435` | full, 2×64, **K=4** | 0.415 → $41,451 | 0.422 → $42,165 | K is a validation knob, not a model knob |
| Width | `115653` | full, **2×128**, K=4 | 0.418 → $41,786 | 0.434 → $43,409 | wider ≠ better |
| Depth | `120939` | full, **3×64**, K=4 | 0.430 → $42,991 | 0.430 → $42,999 | deeper = slightly worse |
| MSE capture | `123043` | full, 2×64, K=4 | 0.414 → $41,375 | 0.421 → $42,123 | + MSE/RMSE + 2 new plots |

### MSE/RMSE readout (run `123043`)

| Metric | Cross-val (K=4) | Held-out test |
|---|---|---|
| MAE (scaled) | 0.414 → $41,375 | 0.421 → $42,123 |
| MSE (scaled) | 0.422 | 0.430 |
| RMSE (scaled) | 0.650 → $64,988 | 0.656 → $65,576 |
| **RMSE − MAE gap** | 0.236 | 0.235 |

---

## PART 3 — Findings

1. **Not capacity-limited.** Width (2×128) and depth (3×64) both left CV MAE
   flat-to-worse relative to the 2×64 baseline. All per-fold scores stayed in the
   ~0.40–0.46 band across every run — differences are within fold-to-fold noise.
2. **K=8 → K=4 changed nothing meaningful** (~$300 CV, ~$700 test). K governs the
   *validation procedure*, not the model; K=4 just runs fewer, larger-fold models.
3. **RMSE ≈ 1.6× MAE, stably** (CV gap 0.236, test gap 0.235). Because RMSE
   squares errors before averaging, this gap is the quantitative signature of a
   few large misses dominating — not a broad uniform spread.
4. **Tail compression, confirmed and worsening with capacity.** The recurring
   worst residual — a ~$1.04M block group — was predicted ~$427K (2×64) →
   ~$400K (2×128) → ~$393K (3×64). MSE-trained models systematically underpredict
   rare high-value neighborhoods, and extra capacity pushes them *lower*.
5. **Conclusion for the write-up:** the ceiling is set by the signal in the 7
   features + MSE's tail behavior, not by model size. This ties all five runs
   into one coherent narrative.

---

## PART 4 — Artifacts

- **Run logs:** `outputs/run_log_<stamp>.txt` (full console capture per run)
- **Plots per run:** `nc_housing_val_mae[_truncated]`, `nc_housing_residuals`,
  `nc_housing_pred_vs_actual` — plus, from run `123043` onward,
  `nc_housing_val_mse[_truncated]` (6 PNGs total).
- Every artifact in a run shares one timestamp; no run overwrites another.

---

## PART 5 — Current state & open items

**Code state:** model = 2×64 ReLU baseline; K=4; MSE/RMSE captured and plotted at
all three stages (K-fold pass 1, per-epoch pass 2, final test eval).

| Priority | Open item |
|---|---|
| LOW | Read the turnaround epoch off the (now sharper) **MSE** curve and pass `--final-epochs N` instead of the default 50 |
| LOW | Stale docs: header lines 15–21 and the `get_model` "UNCHANGED from v1" comment predate the architecture + MSE work — clean up for the write-up |
| LOW | `--quick` epoch fix is only partially applied (pass 1 still uses 10; passes 2/3 use 30) |

*Source: run logs `20260716_105549` through `20260716_123043` and this session's
tool transcript.*
