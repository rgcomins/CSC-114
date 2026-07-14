# SITREP — CSC 114 Module 5/6 Session
**Classification:** UNCLASSIFIED // FOR ACADEMIC USE**
**DTG:** 08 JUL 2026
**Subject:** NC Housing Dataset Deep-Dive + Regression Script Build
**Prepared for:** Rick (CSC 114, Section 1001)

---

## BLUF
Moved from dataset understanding into hands-on build work. Walked the full NC Housing attribute set, confirmed the block-group-vs-individual-home prediction limit, and nailed down exactly what's wrong with `total_rooms` (unrecoverable — wrong ACS table pulled, not a repair candidate). Built a full regression script reskinning the Chapter 4 California Housing example onto NC data. Hit and fixed a real runtime bug along the way: phantom trailing columns in the raw CSV were silently wiping the entire dataset via `dropna()`.

---

## SITUATION

Continuing the Housing Reskin mini-project (NC Housing replacing California Housing). Today's work sits at the boundary of Inception and Iteration 1 — dataset understanding feeding directly into the first working script, ahead of formal backlog issue write-ups.

---

## TASKS COMPLETED

| # | Task | Outcome |
|---|---|---|
| 1 | Confirm dataset download source | Direct URL: `https://dmsenter89.github.io/files/NC_Housing_Prices_2018.csv` — no auth needed |
| 2 | Attribute-by-attribute walkthrough | All 9 documented columns explained, including the three known bugs (rooms/bedrooms dupe, `9999` sentinel, bad `housing_median_age`) |
| 3 | Clarify prediction granularity | Confirmed: model predicts block-group (neighborhood) median value, not individual home price — same limitation as California Housing |
| 4 | Diagnose `total_rooms` bug fully | Both `total_rooms` and `total_bedrooms` were pulled from ACS table B25041 (bedrooms) — `total_rooms` isn't repairable, just unrecoverable; correct fix is to drop it, not fix it |
| 5 | Design the four-issue cleaning fix | Concrete code + a stated order of operations (drop `total_rooms` → mask/drop `9999` target rows → drop bad age row → handle remaining NaNs last) |
| 6 | Build `nc_housing_regression.py` | Full script adapting the Ch.4 CA Housing example: NC-specific cleaning, PyTorch backend (matches class stack), K=8 fold CV (matches Module 4 modification), dollar-formatted predictions, training-curve plots, plus new predicted-vs-actual scatter and residual histogram |
| 7 | Diagnose runtime failure | `dropna()` was returning 0 rows — root cause: phantom `Unnamed: 8/9/10` columns from trailing commas in the raw CSV, undocumented in prior research |
| 8 | Fix the phantom-column bug | Restricted `pd.read_csv()` to an explicit `usecols=KEEP_COLS` allowlist (the 8 trusted columns) so phantom columns never load in the first place |

---

## INCIDENTS / FRICTION ENCOUNTERED

**Incident 1 — Phantom trailing columns in the raw CSV — RESOLVED (workaround), root cause unconfirmed**
The raw NC CSV appears to contain extra columns beyond the 9 documented ones (likely trailing commas per row). This wasn't in the original research doc and first surfaced as a crash (`zero-size array` on `.min()`) after `dropna()` silently dropped every row. Fixed via `usecols` allowlist in the script. **Root cause not yet formally confirmed** — recommended an `awk -F',' '{print NF}' | sort | uniq -c` field-count check, not yet run.

---

## CURRENT STATUS

- `nc_housing_regression.py` — complete, delivered, phantom-column bug fixed. **Not yet confirmed to run clean end-to-end** on the actual file post-fix.
- Final model epoch count — still a placeholder (100) in the script. Needs Rick's own read of the truncated validation MAE curve once a full (non-`--quick`) run completes.
- Root cause of the phantom columns — diagnostic command suggested, not yet run/confirmed.
- Backlog issues (download+store, clean rooms/bedrooms, clean 9999, +1 currency disclaimer) — still in progress from prior session; the phantom-column quirk is a candidate addition to one of these.
- Data-currency disclaimer placement — still an open decision from the prior session.

---

## NEXT ACTIONS

| Priority | Action |
|---|---|
| HIGH | Re-run the script post-fix; confirm row counts survive cleaning and the run completes without errors |
| HIGH | Run the `awk` field-count check to confirm the phantom-column root cause, for the cleaning issue write-up |
| MEDIUM | Do a full (non-`--quick`) run, read the truncated MAE curve, set a real `--final-epochs` value |
| MEDIUM | Finalize and push the backlog issues, folding in the phantom-column quirk if warranted |
| LOW | Decide where the data-currency disclaimer lives (still carried over from the prior session) |

---

*Source: live session — NC Housing attribute walkthrough, cleaning-fix design, and regression script build/debug.*