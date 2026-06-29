# Module 4 — Assess: Explain What You Built
**CSC-114 Artificial Intelligence I**
**Student:** Rick
**Status:** Working draft — 🖊 sections need YOUR words before submitting

> **Note on this document:** Questions marked 🖊 have scaffolding notes below
> them based on our session, but the answer lines are blank. Write those
> yourself. The scaffolding is what we established together — the words have
> to be yours. Questions not yet covered are marked ⚠️ TODO.

---

## Part 1 — Your run

**Q1. Which option did you build, and what one change did you make?**

Option B — California Housing (scalar regression). The one change from the
textbook default: increased K-fold splits from **k=4 to k=8**, which allocates
~87.5% of training data per fold instead of ~75%.

---

**Q2. 🖊 In your own words.** Attach your training curve. At which epoch does
the validation line stop improving? How can you tell from the picture?

> **Scaffolding (do not copy — write your own):**
> - You identified the turnaround at approximately **epoch 48–50**
> - What you're seeing: the curve is still visibly descending through the 30s,
>   then it stops dropping and begins oscillating horizontally around the same
>   MAE value — roughly 0.28–0.30
> - Your curve does NOT show a dramatic uptick after the plateau — it flattens
>   and wobbles rather than rising. That's worth noting in your answer as an
>   honest observation about your specific run.

**YOUR ANSWER:**

_(Write 3–5 sentences in your own words. Name the epoch, describe what the
curve shape looks like before and after that point.)_

---

**Q3. 🖊 In your own words.** What is the model actually doing wrong after
that turnaround point? (Name and explain.)

> **Scaffolding (do not copy — write your own):**
> - The term is **overfitting**
> - What's happening: early in training the model is learning real patterns —
>   bigger houses cost more, better location scores mean higher prices. After
>   the turnaround, it starts fitting the noise and quirks specific to the
>   480 training houses rather than generalizing to new ones.
> - Analogy we used: an analyst who calibrates so tightly to one specific
>   emitter — its hardware drift, operator habits, atmospheric conditions —
>   that their predictions on that source become precise while their
>   performance on any new intercept drops. They memorized the source, not
>   the pattern.
> - Honest caveat for your run: your curve shows a plateau, not a dramatic
>   rise. The overfitting is real but subtle — the averaged K-fold curve
>   masks it.

**YOUR ANSWER:**

_(Write 3–5 sentences. Name it, explain what's actually happening inside the
model, and make an honest observation about what your specific curve shows.)_

---

## Part 2 — Working with your agent

**Q4. 🖊 In your own words.** Describe one moment you corrected or pushed back
on your agent. What did it suggest, what did you do instead, and why?

> ⚠️ **TODO — not covered in session.** Only you know this. Think back through
> your Apply work session:
> - Did the agent suggest accuracy as a metric? (Regression doesn't use accuracy.)
> - Did it try to normalize using test set stats?
> - Did it suggest a different number of epochs?
> - Did it give you something you double-checked against ground_truth_california_housing.md?
> One real moment, described plainly. "I checked X against the ground truth doc
> and found Y" counts as a pushback.

**YOUR ANSWER:**

---

**Q5. Name one thing your agent did well that saved you time.**

> ⚠️ **TODO — your call.** Non-🖊, so you can be direct. Examples from the
> session: generated the K-fold loop structure, wrote the normalization code,
> set up the plot-save logic for headless Codespace operation.

**YOUR ANSWER:**

---

## Part 3 — Why your settings are the right ones

**(Option B — House prices)**

**Q6. 🖊 In your own words.**
- Why does the last layer have no activation (linear output)?
- Why do you measure MAE instead of accuracy, and why normalize using training stats only?

> ⚠️ **TODO — not covered in session.** Use the ground truth doc and our
> Module 3/4 readings to understand these before writing.
>
> Hints to get you started:
>
> **Linear output:** An activation function like sigmoid caps the output
> between 0 and 1. House prices can be any dollar value — $60k, $480k, higher.
> A linear output (no activation) lets the model predict *any* number. Put a
> cap on it and you can never predict a $500k house.
>
> **MAE instead of accuracy:** Accuracy counts right/wrong answers. That only
> makes sense when there are categories — spam or not spam, cat or dog.
> A regression output is a continuous number; there is no "right" answer to
> count. MAE measures how many dollars off you were on average, which is
> meaningful for this problem.
>
> **Training stats only for normalization:** You compute mean and std from
> the training set and apply those same numbers to the test set. If you
> computed stats from the test set, you'd be letting information from the
> test set influence your preprocessing — effectively peeking at the answers
> before the exam.

**YOUR ANSWER:**

---

**Q7. 🖊 In your own words.** Using your own training curve as evidence,
explain why "more epochs = better" is not true for your model.

> **Scaffolding (do not copy — write your own):**
> - Your curve shows the model's validation MAE stops improving around
>   epoch 48–50 and then oscillates flat through epoch 200
> - Running to epoch 200 didn't make the model better on validation data
> - The final model was trained to 130 epochs — stopping at the right time
>   rather than running longer
> - Your curve is good evidence here: point to the flat section and note that
>   every epoch past ~50 produced no additional improvement on held-out data

**YOUR ANSWER:**

_(Write 3–4 sentences. Reference your actual curve and the epoch numbers.)_

---

## Part 4 — Honest self-check

**Q8. 🖊 In your own words.** How much of what you built do you genuinely
understand versus trust your agent on? Name one specific part you'd struggle
to rebuild without help.

> ⚠️ **TODO — only you can answer this.** The rubric rewards specificity and
> honesty over confidence. "I couldn't rebuild the K-fold loop from scratch"
> or "I understand the compile settings but not how backpropagation actually
> computes the gradients" are both strong answers. Vague confidence scores
> lower than honest specificity.

**YOUR ANSWER:**

---

**Q9. 🖊 In your own words.** Explain your model to a classmate in three
sentences: what it takes in, what it predicts, and how it learns.

> ⚠️ **TODO — not covered in session.** Three sentences, plain language.
> Structure: (1) inputs, (2) output, (3) how it improves.
>
> What the model takes in: 8 facts about a California district (size,
> location, income, etc.)
> What it predicts: the median home price for that district in dollars
> How it learns: it makes a guess, measures how wrong that guess was (MAE),
> and adjusts its internal numbers to do better next time — repeated
> thousands of times

**YOUR ANSWER:**

---

## Checklist before submitting

- [ ] All 🖊 answers written in your own words (not this scaffold)
- [ ] Training curve image attached (either the 4-fold or 8-fold PNG)
- [ ] Apply PR link or screenshots included
- [ ] Q4 moment from your actual session — not fabricated
- [ ] Q8 is honest and specific, not vague

---

*Working draft generated from CSC-114 Module 4 Assess session. Scaffolding
provided by course AI assistant. All 🖊 responses must be written by the
student before submission.*
