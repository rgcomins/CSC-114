# Check-In 2: Is It Getting Better? — Sprint 2 Reflection

**Repo/branch link:** TODO — paste your link here (submit separately per
the check-in instructions; documents below should be committed to the same repo)

---

## Before-and-after comparison

**Before (Check-In 1, 7/15 run — `output_07_15.txt`):**
- 8-fold CV mean MAE: 0.414 scaled → ~$41,407 off, on average
- Final test MAE: 0.435 scaled → ~$43,466 off, on average

**After (fix applied — `total_rooms` → `total_bedrooms` in `KEEP_COLS`):**
- TODO — needs a fresh re-run to report a real captured number here. Since
  the two columns hold identical duplicate values in the raw CSV, expect
  the after-number to land very close to the before-number — any
  difference will be run-to-run noise from unseeded model initialization
  (only the train/test split is seeded), not from the fix itself.

*(Say the word if you want a Claude Code handoff brief to grab that
after-number before you finalize this section.)*

---

## Short written reflection (3–4 sentences)

TODO — answer these three questions in your own words. Facts to draw from,
not sentences to copy:

**What did you change since Check-In 1?**
Found and fixed a labeling bug in `nc_housing_model_v1.py`: `KEEP_COLS` was
reading a feature column and calling it `total_rooms`, but that column and
`total_bedrooms` are identical duplicates in the raw CSV (both pulled from
the wrong ACS table, B25041). Fixed the name to `total_bedrooms`.

**Why did you think that change would help?**
Worth being honest here: this wasn't expected to move the error number,
since the underlying values didn't change — only the label was wrong. The
motivation was correctness/trustworthiness of the pipeline (the model was
being documented as using a "rooms" feature it never actually had), not a
performance improvement.

**Did it actually help? How do you know?**
TODO once the after-number is captured. Likely answer: no measurable change
in error, which is the expected and correct outcome given the two columns
were identical — the fix corrects what the model is honestly described as
learning from, rather than changing its accuracy. (Per the assignment's own
note: a change that didn't move the number is a completely legitimate,
reportable result.)

---

## Talking points for your share-out

| Say this | In plain terms |
|---|---|
| What changed | "I tried fixing a column-labeling bug — a feature was being read under the wrong name." |
| What happened | [before/after MAE numbers, once the fresh run is captured] |
| Was it worth it | "Did nothing to the error — expected, since the two columns held identical duplicate values — but it fixes what the model is honestly described as training on." |
| What's next | [one thing — e.g. naive baseline, turnaround epoch, or a real tuning attempt] |
