Module 3 Apply question

Question 1: What loss function does this reading recommend for regression problems, and why?”

GROUNDED: YES  
For regression problems—where you're predicting a number rather than a category—the reading recommends **Mean Squared Error (MSE)**.

The reasoning is simple: MSE works by squaring each mistake before averaging them all together. Think of it like this—if you're off by a little, that's a small penalty, but if you're off by a lot, squaring that error makes the penalty much bigger. This pushes the model to really avoid those big, embarrassing misses rather than just minimizing the average miss casually.

In the house-price example from the reading, that's exactly the setup: the model predicts a dollar amount (any value), so it's a regression problem, and MSE is the natural fit. You'd see this paired in code as:

model.compile(optimizer="adam", loss="mean\_squared\_error")

**Source:** *CSC-114 Module 3 Reading – "How Machine Learning Works,"* Sections 4–5.

Question 2: *“List the five steps of the training loop, in order.”*

The five steps of the training loop, in order:

1. **Feed data** – A batch of houses enters the model.  
2. **Predict** – The model outputs a price guess.  
3. **Compute loss** – One number measuring how far off the guess was.  
4. **Gradient** – Figures out which direction (and how strongly) to nudge each parameter.  
5. **Update parameters** – The optimizer actually makes those nudges.

Then it loops back to step 1 and repeats — often thousands of times — with the loss shrinking a little more each pass.

**Source:** *CSC-114 Module 3 Reading – "How Machine Learning Works,"* Section 8\.

Question 3 *“The reading says a positive gradient means the parameter should increase, right?”* 

Actually, it's the opposite. According to the reading, a **positive** gradient means the parameter should **decrease**, not increase.

Here's the logic: a positive gradient tells you that turning the knob *up* would make the loss *worse*. So to improve things, you turn it *down*. Conversely, a **negative** gradient means turning the knob up would help, so you increase it.

| Gradient value | What it means | What you should do |
| ----- | ----- | ----- |
| Positive (+) | Loss goes up if this knob goes up | **Decrease** the parameter |
| Negative (−) | Loss goes up if this knob goes down | **Increase** the parameter |

A handy way to remember it: the optimizer always moves in the *opposite* direction of the gradient — that's literally the update rule (new value \= old value **minus** learning rate × gradient).

**Source:** *CSC-114 Module 3 Reading – "How Machine Learning Works,"* Section 6\.

Question 4:*“Zero loss is the normal goal we reach on every training run, correct?”* 

Not quite — zero loss is actually described as something that **almost never happens** in real life, not a normal outcome you should expect to hit.

The actual goal of training is simply to make the loss as small as possible — to keep pushing it down, epoch after epoch. In the house-price example, the loss went from $510k off down to $55k off over 40 epochs — solid progress, but not zero. A "perfect" model with zero loss would mean every single prediction matched reality exactly, which essentially never occurs with real-world, messy data.

So the realistic framing is: smaller loss \= better, and you're aiming for "as low as practically achievable," not "all the way to zero."

**Source:** *CSC-114 Module 3 Reading – "How Machine Learning Works,"* Section 5\.

Question 5: *“What exact learning rate value should I use for the house-price model?”* 

The reading doesn't give an exact number for this — and that's actually intentional. Learning rate is something you typically tune by trial and observation rather than read off a chart, since the "right" value depends on the specific model, data, and optimizer.

What it does tell you:

* **Too small** → training creeps along forever  
* **Too large** → the model overshoots and never settles  
* **Just right** → fast, stable progress

Rather than picking a specific learning rate yourself, the practical advice is to start with the **Adam** optimizer, since it adjusts step sizes automatically for each parameter — it's described as "the usual default, start here." That sidesteps a lot of the manual guesswork that picking a raw number would require.

So in code, you'd typically write something like:

model.compile(optimizer="adam", loss="mean\_squared\_error")

...and let Adam handle the step-size tuning rather than specifying a learning rate by hand.

**Source:** *CSC-114 Module 3 Reading – "How Machine Learning Works,"* Section 7\.

Question 6: *“What’s the precise math formula Adam uses to set its step sizes?”* 

The reading doesn't go into that level of detail — it deliberately stays at the conceptual level. It tells you that Adam uses "smart, adaptive step sizes that adjust per parameter" and calls it the sensible default to start with, but it doesn't walk through the underlying formula (which involves tracking moving averages of past gradients and their squares to adjust each parameter's step individually).

For this course, the takeaway the reading wants you to have is simpler: you rarely need to invent or hand-tune an optimizer yourself — picking Adam and moving on is the practical move for most problems.

**Source:** *CSC-114 Module 3 Reading – "How Machine Learning Works,"* Section 7\.

If you want the actual mathematical formula (the moving-average and bias-correction equations), that goes beyond what's in your course materials — happy to look into that separately if it would help, though it's not something you'll need for CSC 114\.

For this course, "use Adam" is enough — you don't need the underlying formula.

Here's why: CSC 114 is an applied course. The course outcomes focus on things like *applying* AI frameworks and *implementing* algorithms — not deriving the math behind them. The reading itself reinforces this by saying you "rarely have to invent an optimizer" and treats Adam as a one-word choice you type into `compile()`, not something to calculate by hand.

So practically speaking: knowing *that* Adam adapts its step size automatically (and *when* to reach for it — basically as your default) is the level of understanding this course expects. The precise formula is the kind of thing you'd only need if you were doing graduate-level ML research or building your own optimizer from scratch.

If you're just personally curious down the road, it's a neat rabbit hole — but it won't show up on anything in CSC 114\.

