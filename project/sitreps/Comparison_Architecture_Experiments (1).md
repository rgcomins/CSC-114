# Comparison — Architecture Experiments (K=4 held fixed)
**NC Housing Price Regression · CSC-114 Module 5/6**

Three architectures, one dial changed at a time from the same baseline. K=4, data cleaning, train/test split (fixed seed), and epoch counts held identical across all three runs.

---

## Head-to-head

| Metric | 2×64 (baseline, `114435`) | 2×128 (width, `115653`) | 3×64 (depth, `120939`) |
|---|---|---|---|
| Per-fold MAE (scaled) | 0.415, 0.404, 0.415, 0.423 | 0.412, 0.399, 0.446, 0.415 | 0.421, 0.417, 0.434, 0.448 |
| Fold range | 0.404 – 0.423 | 0.399 – 0.446 | 0.417 – 0.448 |
| **Mean CV MAE (scaled)** | **0.415** | **0.418** | **0.430** |
| **Mean CV MAE ($)** | **$41,451** | **$41,786** | **$42,991** |
| CV MAE vs. baseline | — | +$335 | +$1,540 |
| **Final test MAE (scaled)** | **0.422** | **0.434** | **0.430** |
| **Final test MAE ($)** | **$42,165** | **$43,409** | **$42,999** |
| Test MAE vs. baseline | — | +$1,244 | +$834 |
| Validation curve minimum | ~flat plateau, no clear minimum | ~epoch 18–20 (~0.409–0.410) | ~epoch 12–15 (~0.409–0.410) |
| Post-minimum trend | flat, noisy | rises into a late spike (~0.4385) | rises into a mid-curve spike (~0.450 near epoch 25), noisier |

---

## Reading the result

**Ranking: baseline < width < depth, on CV MAE.** Neither capacity increase helped. Depth cost roughly 4.6x more CV MAE than width did ($1,540 vs. $335) — the larger of the two effects observed, though each is still a single run.

**On "every fold at or above baseline's range":** not accurate as stated. Two of the depth run's four folds (0.417, 0.421) fall inside the baseline's own observed range (0.404–0.423); only two (0.434, 0.448) exceed it. What *is* true: the depth run's minimum fold (0.417) is higher than the baseline's minimum (0.404), and the mean shift is larger than what the width experiment produced — a real, if more modest than originally stated, signal.

**Statistical caveat, carried forward from the K-fold comparison:** each of these three numbers is a single run. The K=8-vs-K=4 test already showed CV MAE can shift by ~$300 from random weight initialization alone with no architecture change at all. Width's $335 shift is within that noise band. Depth's $1,540 shift is noticeably larger than that noise band, which makes it the more credible of the two effects — but "credible" here still means "consistent with a real effect," not "proven." Repeated trials per architecture would be needed to state this with statistical confidence.

**Residual tail — corrected.** An earlier pass at this comparison claimed the $1.04M block group (row 3358) declined smoothly across all three architectures (~$450K → ~$400K → $393K). The actual width-run prediction for that row was **$449,967** — essentially unchanged from baseline ($453,999) — so there's no width-stage decline for this row; only the depth stage moved it, down to $393,201.

Looking at all three worst-residual rows across all three runs:

| Row | Actual | Baseline (2×64) | Width (2×128) | Depth (3×64) | Pattern |
|---|---|---|---|---|---|
| 3140 | $608,200 | $127,023 | $121,391 | $112,755 | **Monotonic decline** — the clean example, if you want one |
| 3261 | $1,453,800 | $874,332 | $930,602 | $891,855 | Non-monotonic — width improved it, depth partially reversed that |
| 3358 | $1,044,300 | $453,999 | $449,967 | $393,201 | Flat through width, then a real drop at depth |

Only row 3140 supports a clean "capacity makes the tail worse" story at every step. The other two rows complicate it. If the write-up wants a single-row illustration, 3140 is the defensible one to cite; 3358 only tells that story for the depth stage, and 3261 doesn't tell it at all.

**What is well-supported in aggregate:** depth's overall CV and test MAE are both worse than baseline's, and worse than width's CV MAE (though slightly better than width's test MAE, interestingly — $42,999 vs. $43,409). Capacity increases, in this test, did not buy better generalization on this dataset. That conclusion doesn't depend on any single row and holds up under the correction above.

---

## Recommendation

**Close the architecture-experiment thread here.** Three configurations tested, one dial changed at a time, and the baseline (`Dense(64)×2`) comes out ahead on every metric except one (test MAE where depth edges width). Reasonable to state as a working conclusion, with appropriate hedging given single-run measurements: this dataset's ~4,500 training rows and 7 features don't seem to reward extra network capacity, in either direction. Recommend reverting to `Dense(64)×2` as the model carried into the final write-up.

---

*Sources: run_log_20260716_114435.txt (2×64), run_log_20260716_115653.txt (2×128), run_log_20260716_120939.txt (3×64).*
