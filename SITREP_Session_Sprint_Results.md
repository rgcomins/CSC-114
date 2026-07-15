# SITREP — CSC 114 Module 5/6 Session
**Classification:** UNCLASSIFIED // FOR ACADEMIC USE
**DTG:** 15 JUL 2026
**Subject:** NC Housing Model — Sprint Re-run, Results Capture & Reflections
**Prepared for:** Rick (CSC 114, Section 1001) — handoff to homework session

---

## BLUF
Re-ran the K=8 fold NC Housing regression end-to-end (clean, exit 0) and
captured fresh, real numbers. **The model clears both "good enough" bars:**
validation MAE **$41,407** vs. a **~$78,878** predict-the-mean baseline (~47%
lower error), with the validation curve flattening around **epoch ~12–13**.
Regenerated all four plots, added a naive-baseline helper and a controlled
before/after residual figure proving the age-outlier cleanup worked, and wrote
Sprint 1 and Sprint 2 reflections (numeric content filled; graded prose drafted
from your own notes and flagged for your review). All committed to branch
`sprint-results-writeup` (`0ee0fd4`), **not pushed**. Remaining work is your
graded reflection prose, the awk root-cause diagnostic, and a couple of small
data-hygiene loose ends.

---

## SITUATION
Sprint execution session for the Housing Reskin mini-project (Tabular cohort).
Scope was deliberately narrow: **re-run the existing model, record real results,
update the write-up with factual numbers only** — no architecture, feature, or
cleaning changes. Environment is GitHub Codespaces, Keras 3.14.1 on the
**PyTorch backend** (`KERAS_BACKEND=torch`, standalone `import keras`).

---

## TASKS COMPLETED

| # | Task | Outcome |
|---|------|---------|
| 1 | Re-run K=8 fold regression (`nc_housing_model_v1.py`) | Clean end-to-end, exit 0. 5,635 rows survive cleaning. Log: `project/output_07_15.txt` |
| 2 | Record validation/test results | Val MAE **$41,407** (0.414 scaled); test MAE **$43,466** (0.435). Per-fold: [0.418, 0.425, 0.387, 0.411, 0.435, 0.415, 0.398, 0.424] |
| 3 | Compute naive baseline | `project/naive_baseline.py` (reuses model's exact load/split/scale): **~$78,878** k-fold, ~$77,808 test |
| 4 | Identify turnaround epoch | Validation MAE flattens **~epoch 12–13**; then oscillates in a noisy ~0.403–0.427 band (global min ≈ epoch 22, within noise) |
| 5 | Regenerate all 4 plots | `nc_housing_val_mae.png`, `nc_housing_val_mae_truncated.png`, `nc_housing_pred_vs_actual.png`, `nc_housing_residuals.png` (all in `project/`) |
| 6 | Controlled before/after A/B | `project/before_after_residuals.py` — toggles ONLY the `age==2000` rows: test MAE **$54,370 → $44,522** (~18%), worst error **$6.77M → $594K**. Figure: `project/nc_housing_residuals_before_after.png` |
| 7 | Update charter | Filled "Definition of good enough" with measured numbers + plot links |
| 8 | Write reflections | `Sprint 1 Reflection.md` + `Sprint 2 Reflection.md` — numeric content filled; graded prose drafted from `nc_housing_notes_v1/v2.md`, flagged for your review |
| 9 | `total_rooms` allowlist review | See Incident 3 — confirmed mislabel (not wrong data); fixed docs only, no behavior change |
| 10 | Commit | Branch `sprint-results-writeup` (multiple commits; see `git log`). **Not pushed to origin.** |

---

## INCIDENTS / FRICTION ENCOUNTERED

**Incident 1 — Misleadingly-named data file.**
`project/NC_Housing_Prices_2018_age_cleaned.csv` still contains the 2
`housing_median_age == 2000` rows. Root cause: `clean_age_outliers.py` filters
`== 2018`, not `== 2000`. The actual age-2000 removal happened downstream in
`NC_Housing_Prices_ready.csv` (confirmed 0 such rows, max age 78). Not blocking —
the model runs on the "ready" file — but the filename is a trap for future you.

**Incident 2 — Long CPU-bound run time.**
The full (non-`--quick`) K=8 run trains 17 models and took ~18 min on Codespaces
CPU. Fine, just plan for it; use `--quick` for smoke tests.

**Incident 3 — `total_rooms` vs `total_bedrooms` allowlist — CONFIRMED mislabel, RESOLVED (docs only).**
`KEEP_COLS` allowlists `total_rooms`, the column the notes flagged as the
unrecoverable B25041 duplicate. BUT verified empirically: in the raw file that
carries both, `total_rooms` and `total_bedrooms` are **byte-for-byte identical**
(0 differing rows) — both are the same B25041 bedroom counts. So this is a
**mislabeling** issue, not "training on wrong data" — the numbers are correct,
the name is not. The originally-proposed one-line swap (`total_rooms` →
`total_bedrooms`) would **crash** the default run: `NC_Housing_Prices_ready.csv`
(argparse default) has `total_rooms` and no `total_bedrooms`, and `usecols`
raises on a missing column. Switching to the docstring's `age_cleaned.csv` to
get `total_bedrooms` would reintroduce the age≈2000 outliers (Incident 1).
**Resolution chosen:** keep `total_rooms` in `KEEP_COLS`, fix the stale/backwards
comment + docstring to say the column really holds bedroom counts, and align the
docstring's Run/Data lines with the actual filename. Zero prediction change.

---

## CURRENT STATUS
- Model runs clean and **meets both charter "good enough" criteria.**
- Both reflections and the charter carry real numbers.
- Work committed to a feature branch; **nothing pushed to origin.**
- Final-model epoch count still uses the script default (50), not explicitly
  set to the read-off turnaround (`--final-epochs` unused).

---

## NEXT ACTIONS

| Priority | Action |
|----------|--------|
| HIGH | **Write your own graded reflection prose** — the "what runs / what's broken / on track" answers (Sprint 1) and the change/why/did-it-help answers (Sprint 2) are drafted from your notes but must be reviewed, edited, and owned by you before submission |
| HIGH | Decide push/PR: `git push -u origin sprint-results-writeup` then `gh pr create`, or merge to `main` locally |
| MEDIUM | Run the awk trailing-comma diagnostic: `awk -F',' '{print NF}' raw.csv \| sort \| uniq -c` — confirm the phantom-column root cause for the cleaning issue write-up (separate, unblocked) |
| MEDIUM | Set `--final-epochs` to the turnaround (~12–13) for the final model instead of the 50 default |
| LOW | Rename/annotate `NC_Housing_Prices_2018_age_cleaned.csv` so the name matches what it actually contains |
| LOW | Finalize where the data-currency disclaimer (2018 ACS ≈ 2023) lives |
| LOW | Consider whether the legitimate high-value Charlotte properties are worth any modeling effort (currently out of scope) |

---

## KEY FILES / REFERENCES
- Model: `project/nc_housing_model_v1.py` (K=8, PyTorch backend)
- Data (in use): `project/NC_Housing_Prices_ready.csv` (5,637 rows, `total_rooms` label)
- Run log: `project/output_07_15.txt`
- Baseline helper: `project/naive_baseline.py`
- Before/after A/B: `project/before_after_residuals.py`
- Write-ups: `charter.md`, `Sprint 1 Reflection.md`, `Sprint 2 Reflection.md`
- Prior notes: `project/nc_housing_notes_v1.md`, `project/nc_housing_notes_v2.md`
- Branch/commit: `sprint-results-writeup` @ `0ee0fd4` (unpushed)

---

*Source: live session — full model re-run, results capture, controlled
outlier-removal A/B, and reflection/charter write-up.*
