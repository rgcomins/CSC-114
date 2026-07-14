# CSC-114 Module 5: Inception — Starting the Mini-Project
## Instructor Outline

| Field | Value |
|-------|-------|
| Course | CSC-114 (follows CSC-113 AI Fundamentals) |
| Module | 5 — Inception: Starting the Mini-Project |
| Position | First of four project modules (5 → 8): Inception → Iteration 1 → Iteration 2 → Release |
| Duration | 2 meetings, each a 2-hour block — **4 contact hours total** |
| Meeting structure | Hour 1 = lecture, Hour 2 = lab *(provisional — adjust to the room)* |
| Spine | Chollet workflow chapter (universal ML workflow) as the process map |
| Prerequisites | Module 4 complete: students have trained, validated, and diagnosed overfitting on California Housing |
| Cohorts | Tabular · Image · NLP · Agent (agent cohort runs the process layer only, off-textbook) |
| Team size | Solo or pairs |
| Student-facing handouts | *Project Charter* template; *Definition of Good Enough* worksheet; *Agent Guardrails* starter |
| Status | DRAFT — outline for review before student handouts are written |

---

## Where This Module Sits

This is the pivot. For four modules students followed the textbook chapter-by-chapter; now the textbook stops driving and the **project** drives, with Chollet's workflow chapter demoted from "a chapter to cover" to "the map we navigate by." Modules 5–8 are one project built in four iterations.

Module 5 is almost entirely the **universal process layer** — the part every cohort shares regardless of domain. The technical work that differs by cohort doesn't really start until Module 6. That's deliberate: it keeps the pivot low-whiplash and puts the process scaffolding where it does the most good, at the very start, before anyone is deep in domain-specific weeds.

The one place the module branches four ways is the final lab step, *defining "good enough."* Everything up to that point is identical for all cohorts.

---

## The Anti-Whiplash Bridge (read this first)

Students spent last week in implement mode on California Housing. Do **not** open Module 5 by introducing a new project. Open it by renaming the old one:

> "You already did a mini-project. You picked a problem, trained a model, watched it overfit, and figured out where to stop. That *was* one turn through a process — you just didn't give the process a name. Today we name it. Then you'll point the same process at a problem you choose."

The Practice block (Meeting 1, Hour 2) is built entirely around this: students fill out a project charter for the California Housing work **they already finished**, before they ever charter something unknown. They practice the template on familiar ground first. Protect this time — it is the bridge, and rushing to new-project selection is the main way this module goes wrong.

---

## Learning Targets

By the end of Module 5, a student can:

1. **Explain** the difference between *doing tasks* and *running a project* — a project has a goal, a definition of done, and a record — and name the handful of XP values that keep a small project healthy (small releases, continuous feedback, simplicity, courage to throw away what isn't working).
2. **Recognize** their California Housing work as one completed turn through the universal workflow, and name which step they were on when they stopped.
3. **Write** a one-page project charter: problem (or task), domain, data/tools, and a written definition of "good enough."
4. **Translate** "good enough" into a concrete, measurable success signal appropriate to their cohort (a metric + evaluation protocol for the ML cohorts; the three-test set for the agent cohort).
5. **Stand up** the project repository with Sacred Flow scaffolding: README, a seeded issue backlog framing the walking skeleton, and an agent-guardrails doc that keeps their AI assistant on task.

---

## LPAA Structure

Only **Assess** is rubric-graded; Learn / Practice / Apply are formative.

### Learn — Meeting 1, Hour 1 (lecture, kept short and intuition-first)

Four ideas, in order. Resist adding a fifth.

- **You already did this.** Walk the class back through California Housing as a project: there was a problem, a way to measure success (MAE), a way to check honestly (k-fold), and a moment you decided it was good enough (the curves stopped improving). That is the whole shape.
- **Tasks vs. projects.** A task is a thing you do. A project is a thing you *finish* — which means it needs a goal you agreed on up front and a record of how you got there. The Sacred Flow (Issue → Branch → PR → Review → Merge) is what keeps the record.
- **XP in four values.** Not the whole methodology — just: ship small and often; get feedback constantly; do the simplest thing that could possibly work; and have the courage to delete code that isn't working. That's the whole XP lecture.
- **Decide "good enough" before you build.** The single most important habit in the module. Chollet's workflow makes you choose a measure of success *before* modeling for a reason: it's what stops you from polishing forever, and it's the same discipline that told you when to stop training on Housing. If you don't define done, you never are.

Close by showing the four-module arc as the map:

| Module | Plain-language goal | Workflow spine step |
|--------|--------------------|--------------------|
| 5 — Inception | Decide what we're building and how we'll know it's good | Define problem, metric, evaluation protocol |
| 6 — Iteration 1 | Make it run, badly (end-to-end) | Prepare data, dumb baseline, first model that beats it |
| 7 — Iteration 2 | Make it good | Scale up, regularize, tune |
| 8 — Release | Ship it and reflect | Package, document, demo |

### Practice — Meeting 1, Hour 2 (lab: the CA Housing retro)

Guided, whole-class or in pairs. Students complete a charter for the California Housing project they **already built**:

- **What we built:** predict median house value for California districts.
- **Data/tools:** the California Housing dataset; Keras; k-fold validation.
- **Definition of good enough:** beats the naive baseline; validation MAE stops improving (the turnaround epoch).
- **What step did we stop on?** Most will land on "scale up / regularize" — the honest answer is that the canned script ran *past* the turnaround, which is exactly the pedagogical hook from Module 4.

The point is transfer: they run the template once on something they understand cold, so that when they run it on an unknown project in Meeting 2, the tool is already familiar and their attention is free for the *thinking*.

### Apply — Meeting 2 (the real thing)

- **Hour 1 — Charter their own project.** Form pairs (or commit to solo), pick a cohort, and draft an original charter using the template. Instructor circulates to pressure-test scope — over-scoping is the #1 novice failure and the "What we are NOT doing" line is the fix.
- **Hour 2 — Stand up the repo.** README from template; seed 3–5 backlog issues that describe the walking skeleton (Module 6's target); commit the agent-guardrails doc. Code Builders do this through the full Sacred Flow; Prompt Masters run the same GitHub flow with their configs/prompts as the artifacts.

**The four-way branch lives here, at "define good enough":**

| Cohort | "Problem statement" becomes | "Definition of good enough" becomes |
|--------|----------------------------|-------------------------------------|
| Tabular | Predict/classify target *X* from dataset *Y* | Metric (e.g., MAE / accuracy) + evaluation protocol (train/val split or k-fold) + a threshold that beats baseline |
| Image | Classify images into categories *C* | Same as tabular, plus a realistic note on dataset size / download cost for Codespaces |
| NLP | Classify/generate text for task *T* | Same as tabular, on a text-appropriate metric |
| Agent | Define the *task* the agent performs | The **three-test set** (known-good, trap, edge) *is* the evaluation protocol; the test cases are the "data" |

### Assess — Graded artifacts (Complete/redo, Developing-to-Proficient band)

Committed to the repo under `module5/`:

1. `charter.md` — problem/task, cohort, data/tools, definition of good enough, scope guard, roles.
2. **Issue backlog** — 3–5 issues framing the walking skeleton, in the student's own words.
3. `agent-guardrails.md` — the doc that keeps their AI assistant on task (the sacred-workflow material, applied to *their* project).
4. `reflection.md` — a short note connecting California Housing to the new project: which workflow step were you on when you stopped last time, and what's different this time?

Rubric emphasis for Module 5 is weighted toward **Problem-Solving Process** (did they define "good" *before* building?) and **Professional Communication** (is the charter legible to someone who isn't them?). AI Partnership Quality and Critical Thinking are lightly assessed here and grow in weight across Modules 6–8.

---

## The Charter Template (student-facing, ~10th-grade)

```markdown
# Project Charter: [project name]

## What we're building (one sentence)
[Plain language. "An app that..." or "A model that..." or "An agent that..."]

## Cohort
[ Tabular / Image / NLP / Agent ]

## The data or tools we'll use
[Dataset name and where it comes from — or, for the agent cohort,
the tools and instructions the agent will rely on.]

## Definition of "good enough"
Before we build, we agree this project is good enough when:
- [a signal we can actually measure]
- [a second signal we can actually measure]

## What we are NOT doing (scope guard)
[List 2-3 tempting things you are choosing to leave out. This is where
you protect yourselves from building forever.]

## Team & roles
[Solo, or two names. If a pair: who reviews whose pull requests?]
```

---

## Instructor Appendix — NOT for student distribution

```text
=== MODEL CHARTER: California Housing (for the Practice retro) ===
What we built:  A model that predicts median house value for a
                California district from its features.
Cohort:         Tabular.
Data/tools:     California Housing dataset; Keras; k-fold validation.
Good enough when:
                - Validation MAE beats the naive (predict-the-mean) baseline.
                - Validation MAE stops improving (the turnaround epoch).
Not doing:      Feature engineering beyond what's provided; deployment.
Stopped on:     "Scale up / regularize." Honest note: the provided script
                ran PAST the turnaround epoch — that was the Module 4 hook.

=== RUBRIC MAPPING (four-category) ===
charter.md            -> Problem-Solving Process (primary),
                         Professional Communication
issue backlog         -> Problem-Solving Process
agent-guardrails.md   -> AI Partnership Quality
reflection.md         -> Critical Thinking & Ethics,
                         Problem-Solving Process
Weekly band: Developing-to-Proficient, Complete/redo.

=== LIKELY-CONFUSED ITEMS ===
- "Definition of good" vs. "the metric." The metric is the ruler;
  the definition of good is the threshold you draw on the ruler.
  A charter needs BOTH.
- Agent cohort asking "where's my dataset?" -> Their test cases ARE
  the data. The three-test set is their evaluation protocol.
- Over-scoping. Novices write charters they can't finish in three
  iterations. The "What we are NOT doing" line is the intervention —
  make them fill it in during Hour 1, not after.
- Pairs treating review as a rubber stamp. Reviewing is graded work;
  see Professional Communication.

=== FOUR-WAY "DEFINE GOOD ENOUGH" CHEAT SHEET ===
Tabular/Image/NLP: metric + evaluation protocol + baseline-beating
                   threshold. (Chollet workflow steps 1-3.)
Agent:             task definition + three-test set (known-good,
                   trap, edge). Test cases replace "dataset."

=== FAST-MOVING-TARGET FLAGS (re-verify each term) ===
- Image/NLP dataset availability and download size vs. Codespaces
  disk/bandwidth. A devcontainer.json preinstalling extensions +
  keras keras-hub jax would remove most of this friction class-wide.
- Agent platform/model names and free-tier terms.

=== OPEN DESIGN DECISIONS TO CONFIRM ===
- How the two tracks (Code Builders / Prompt Masters) map onto the
  four cohorts for the mini-project. Working assumption: tracks
  govern submission mechanics (what the artifacts are + how they're
  committed), not the work itself. Confirm before writing handouts.
- Whether pairs must be same-cohort. (Recommend yes — cross-cohort
  pairs double the support surface.)
- devcontainer.json rollout timing.

=== ESCALATION CONTACTS ===
Mallory Milstead · Andrew Norris

=== INSTRUCTOR NOTE: PROTECT THE RETRO ===
The Practice block (CA Housing charter) is the anti-whiplash bridge.
Do not compress it to get to new-project selection faster. Students
who charter familiar work first transfer the skill; students who
skip straight to their own project stall on the blank page.
```
