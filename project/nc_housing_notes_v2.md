# Session Summary — NC Housing Model, Outlier Investigation
**Date:** July 13, 2026
**Course:** CSC 114, Section 1001

---

## What we were looking into

Our model's error chart (the residual plot) looked off — most of the errors were bunched near zero, but the chart stretched way out to the right, which meant a few predictions were wildly wrong. We set out to figure out why.

## What we found

There were two different kinds of outliers, and they turned out to have two different explanations:

**1. Bad data — confirmed and fixable.**
Two rows in the dataset listed a house's age as 2000 years old. That's obviously a data entry error, not a real house. These rows were skewing the model's training, so the plan is to **remove them** before the next run.

**2. Not bad data — a real, unusual house.**
A separate outlier turned out to be a legitimate expensive home in the Charlotte area — the model just didn't predict its price well. We traced this one back to the original spreadsheet and confirmed the numbers are accurate; the house is just genuinely unusual (very high income and value for the area), and the model struggled to guess it correctly. This isn't a data problem — it's a case where the model needs more work to handle unusual, high-end properties.

## Where things stand

- The model's k-fold results are coming back fairly consistent across folds, which is a good sign the setup itself is stable.
- Training is currently locked to 50 epochs, mainly to keep runs fast while we debug.

## Plan for next session

1. Remove the two bad-age rows and re-run the model.
2. Take a closer look at the legitimate outlier (the expensive Charlotte house) and think through why the model missed it and whether anything can be done about it.

