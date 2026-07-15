# Sprint 1 Reflection — Check-In 1: Is It Alive?

*(Assignment says "Spring 1 Reflection" — likely means "Sprint 1." Rename the file
to match whatever the assignment drop actually expects, if different.)*

## What actually runs right now?

TODO — write this in your own words. Facts to draw from, not sentences to copy:
- K=8 regression script runs end-to-end without errors (confirmed 7/15 run,
  `output_07_15.txt`)
- Input: 5,637 raw rows → 5,635 after cleaning; 4,508 train / 1,127 test
- 8-fold CV mean MAE (scaled): 0.414 → **~$41,407 off, on average**
  (per-fold range 0.387–0.435 — tight, no fold wildly off)
- Final model test MAE: 0.435 → **~$43,466 off, on average**
- Output: dollar-formatted predictions + all 4 required plots saved
  (`nc_housing_val_mae.png`, `nc_housing_val_mae_truncated.png`,
  `nc_housing_pred_vs_actual.png`, `nc_housing_residuals.png`) — plus a bonus
  before/after ablation plot on the housing_median_age fix
  (`nc_housing_residuals_before_after.png`): test MAE $54,370→$44,522,
  worst-case error $6.77M→$593,503 after removing the bad-age rows

## What's still missing or broken?

TODO — write this in your own words. Things to consider:
- Root cause of the trailing commas in the raw CSV isn't confirmed yet — the
  `usecols` allowlist works around it, but the awk field-count diagnostic to
  find *why* they're there hasn't been run
- **Needs verification:** today's raw columns are
  `[population, households, median_income, median_house_value, total_rooms,
  latitude, longitude, housing_median_age]` — `total_rooms` is present and
  used as a feature, and `total_bedrooms` isn't loaded at all. That's the
  reverse of the documented decision (total_rooms was the one flagged as an
  unrecoverable duplicate — meant to be dropped, not kept). Worth checking
  the `usecols`/`KEEP_COLS` list before this goes further.
- **Needs reconciling:** the log shows 0 rows dropped by the "bad
  housing_median_age" filter this run (5,635 → 5,635), but the before/after
  ablation plot shows that filter mattering a lot elsewhere. Possibilities:
  the locally-stored CSV was already cleaned upstream (so nothing's left to
  drop at runtime), or the filter condition isn't matching. Worth a quick
  sanity check, not urgent for this check-in.
- Naive (predict-the-mean) baseline hasn't been computed yet — needed to
  satisfy the charter's "definition of good enough"
- Turnaround epoch (where validation MAE flattens) hasn't been read off the
  curve and named yet — same charter requirement
- Two of the three worst residuals involve six-figure `median_income`
  values, including one at exactly $250,010 — ACS commonly top-codes income
  at $250,001, so that row may be a top-coded outlier rather than a genuine
  data point; worth a note if it comes up

## Are you still on track with the scope from your charter?

TODO — write this in your own words. Check against `charter.md`:
- "Definition of good enough" has two parts: beat the naive baseline (not
  computed yet) and name the validation-MAE turnaround epoch (not read off
  the curve yet) — both still open, not blockers for this check-in
- "What we are NOT doing" scope guard: no general ACS cleaning pipeline, no
  re-deriving features from the raw Census API, no deployment/UI — has
  anything crept outside this?

---

## Share-out talking points (prep only — not part of the submission)

| Say this | In plain terms |
|---|---|
| What I'm building | [one sentence, from your charter] |
| What runs today | "Right now it takes ___ and gives back ___." |
| What's broken or missing | [be honest — e.g. trailing-comma root cause TBD] |
| What you're doing next | [one thing — e.g. run the awk diagnostic] |
