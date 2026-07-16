# Comparison — Width 64 vs. Width 128 (K=4 held fixed)
**NC Housing Price Regression · CSC-114 Module 5/6**

Single change tested: hidden layer width only (`Dense(64)` → `Dense(128)`, both hidden layers). K=4, data cleaning, train/test split (fixed seed), and epoch counts held identical across both runs.

---

## Head-to-head

| Metric | Width 64 (`114435`) | Width 128 (`115653`) | Difference |
|---|---|---|---|
| Per-fold MAE (scaled) | 0.415, 0.404, 0.415, 0.423 | 0.412, 0.399, 0.446, 0.415 | — |
| **Mean CV MAE (scaled)** | **0.415** | **0.418** | **+0.003** |
| **Mean CV MAE ($)** | **$41,451** | **$41,786** | **+$335** |
| **Final test MAE (scaled)** | **0.422** | **0.434** | **+0.012** |
| **Final test MAE ($)** | **$42,165** | **$43,409** | **+$1,244** |
| Validation curve shape | Noisy, essentially flat plateau from ~epoch 15 on | Minimum ~epoch 18–20, then a rising trend into a late spike | width-128 shows the first clear overfitting shape in this project |
| Worst-residual rows | 3140, 3261, 3358 | 3140, 3261, 3358 | identical rows |
| Worst-residual errors | −$481K / −$579K / −$590K | −$487K / −$523K / −$594K | mixed — one better, two worse |

---

## Reading the result

**CV MAE: a wash.** The $335 gap is within the noise band already established by the K=8-vs-K=4 comparison ($311 gap there, attributed to randomness). Width alone didn't move this number in any way worth trusting as a real effect.

**Test MAE: moved further, and in the wrong direction.** A $1,244 rise on a single run isn't proof by itself, but it's not an isolated number either — it agrees with what the validation curve shows.

**The curve is the real story this run.** Every prior run — width-64 at both K=8 and K=4 — plateaued noisily without a clear rising trend. This is the first run where validation MAE bottoms out (~epoch 18–20) and then climbs, ending in a sharp late spike. That shape is the textbook overfitting signature from the Chapter 3 material: train loss still falling while validation stalls and reverses. Doubling the width handed the model roughly 4x the parameters in each hidden layer — more capacity than this ~4,500-row training set can support without starting to memorize.

**This matches the caution raised before the experiment.** Going into this test, the concern was that tabular data with a handful of features doesn't usually need much capacity, and extra width on a small dataset raises overfitting risk faster than it raises accuracy. That's what happened here — capacity went up, generalization (as measured by test MAE) went down.

**Residual tail:** the same three block groups remain the worst misses either way, with mixed movement in magnitude — width didn't fix or worsen the MSE tail-compression effect in any consistent direction. That behavior looks like it's driven by the loss function and the rarity of high-value rows, not by model capacity.

---

## Recommendation

**Do not adopt width=128.** It did not improve the CV estimate, it made the held-out test performance measurably worse, and it's the first run showing a real overfitting signature. `Dense(64)×2` remains the better-supported choice for this dataset size.

**Silver lining:** this run is also the first with a curve clean enough to point to a candidate turnaround epoch (~epoch 20) — useful if you want to cite it as evidence for what an overfitting turnaround *would* look like on this project, even though the final model you keep will likely stay at width 64.

**If there's time for one more test:** depth (adding a third hidden layer at 64 units, rather than widening) is the other originally-discussed dial, and hasn't been tested yet.

---

*Sources: run_log_20260716_114435.txt (width 64) and run_log_20260716_115653.txt (width 128), this session.*
