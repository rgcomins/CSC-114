# CSC-114 Module 5 — Mini-Project Quickstart (GameFAQs Style)

```
================================================================================
              CSC-114 ARTIFICIAL INTELLIGENCE I  --  MINI-PROJECT
                   MODULE 5: INCEPTION  --  QUICKSTART FAQ
                          "How To Start Without Panicking"
                                By: TeachTechTerry
                             Last Updated: 07/01/2026
                       Platform: GitHub Codespaces / Your Repo
================================================================================

     __  __  ___  ____  _   _ _     _____   ____
    |  \/  |/ _ \|  _ \| | | | |   | ____| | ___|
    | |\/| | | | | | | | | | | |   |  _|   |___ \
    | |  | | |_| | |_| | |_| | |___| |___   ___) |
    |_|  |_|\___/|____/ \___/|_____|_____| |____/

    [ INCEPTION -- DRAW YOUR FINISH LINE BEFORE YOU BUILD ]

================================================================================
TABLE OF CONTENTS
================================================================================

  0.0 - WHAT IS THIS DOC
  1.0 - START HERE (YOU ARE NOT A NEW PLAYER)
  2.0 - CHARACTER CREATION (PICK YOUR PATH)
  3.0 - THE CAMPAIGN MAP (4 LEVELS)
  4.0 - LEVEL 5 WALKTHROUGH (WHAT YOU DO THIS WEEK)
  5.0 - THE COMBAT SYSTEM (THE SACRED FLOW)
  6.0 - BOSS FIGHT: "GOOD ENOUGH"
  7.0 - WAYS TO GET A GAME OVER (AND HOW TO AVOID THEM)
  8.0 - SECRET: NEW GAME+ (THE HOUSING RESKIN)
  9.0 - SAVE POINTS (WHAT TO TURN IN)
  X.0 - CREDITS & LEGAL

================================================================================
0.0 - WHAT IS THIS DOC
================================================================================

This is your quickstart for the mini-project you'll build across the last four
modules of the course. It tells you how to BEGIN. It does not tell you every
answer -- that's your job, with your AI partner riding shotgun.

Read sections 1-4 before class. Come back to 5-9 when you're stuck.

================================================================================
1.0 - START HERE (YOU ARE NOT A NEW PLAYER)
================================================================================

Deep breath. You already beat a level like this.

Last week you trained a model on California Housing. You picked a problem, you
measured how good it was, you checked yourself honestly, and you decided when
to stop. That IS a project. Nobody called it one. We're calling it one now.

So this module is not a fresh start. It's the same moves, pointed at a project
YOU choose. If you finished Housing, you can finish this.

================================================================================
2.0 - CHARACTER CREATION (PICK YOUR PATH)
================================================================================

Two choices to make before anything else.

  PARTY SIZE:
    [ ] Solo run        -- you, your repo, your reviews (self-review counts)
    [ ] Co-op (2 players) -- you review each other's pull requests for real

  YOUR PATH (pick ONE):
    > TABULAR .... rows and columns. Closest to Housing. Safest pick.
    > IMAGE ...... classify pictures. Watch your dataset size in Codespaces.
    > NLP ........ work with text. Classify it or generate it.
    > AGENT ...... extend your Module 1 agent. Your test cases are your "data."

  RULE: if you go co-op, both players pick the SAME path. No mixed parties.

  Not sure? Pick TABULAR and reskin the Housing project on a new dataset.
  That's not the easy-mode cop-out -- it hits every scoring category. It's smart.

================================================================================
3.0 - THE CAMPAIGN MAP (4 LEVELS)
================================================================================

  LVL 5  INCEPTION ...... Decide what you're building + how you'll know it's good
  LVL 6  ITERATION 1 .... Make it RUN. Badly is fine. Just end-to-end.
  LVL 7  ITERATION 2 .... Make it GOOD. Now you tune and improve.
  LVL 8  RELEASE ........ Ship it. Document it. Demo it.

  You are here: LVL 5. Do NOT try to build a good model this week. That's LVL 7
  you're thinking of. Wrong level. Slow down.

================================================================================
4.0 - LEVEL 5 WALKTHROUGH (WHAT YOU DO THIS WEEK)
================================================================================

Four steps. In order.

  STEP 1 -- WRITE THE CHARTER (charter.md)
    One page. Fill in the template your instructor hands out:
      - What you're building, in one sentence
      - Your path
      - The data or tools you'll use
      - Your DEFINITION OF "GOOD ENOUGH" (see section 6.0 -- this is the fight)
      - "What we are NOT doing" (list 2-3 tempting things you're skipping)
      - Team + who reviews whose PRs

  STEP 2 -- STAND UP THE REPO
    README from the template. This is your save file. Name it like a human.

  STEP 3 -- SEED THE BACKLOG (3 to 5 ISSUES)
    Write 3-5 GitHub Issues describing the FIRST WORKING VERSION (that's LVL 6).
    In your own words. These are your quest log.

  STEP 4 -- COMMIT THE GUARDRAILS DOC (agent-guardrails.md)
    Write down the rules that keep your AI partner on task: what it's allowed
    to do, what it must never do, and how you'll check its work. An agent with
    no guardrails wanders off and does side quests you didn't ask for.

That's the whole level. No model. Just a finish line and a repo.

================================================================================
5.0 - THE COMBAT SYSTEM (THE SACRED FLOW)
================================================================================

You already know this. It never changes:

    ISSUE  ->  BRANCH  ->  PR  ->  REVIEW  ->  MERGE

  - NEVER commit straight to main. Not once. Main is sacred.
  - Every piece of work starts as an Issue.
  - You do the work on a branch, in a Codespace.
  - You open a Pull Request when it's ready.
  - Someone reviews (co-op = your partner; solo = you, in writing, or your AI
    partner as a rubber duck -- document it in the PR).
  - Then, and only then, you merge.

  Messy code inside a branch is FINE. That's what branches are for. The process
  is the safety net; the code can be a beautiful disaster until review.

================================================================================
6.0 - BOSS FIGHT: "GOOD ENOUGH"
================================================================================

This is the boss of Level 5, and it kills more projects than any bug.

    IF YOU DON'T DEFINE "DONE," YOU NEVER ARE.

Decide what "good enough" means BEFORE you build. Write it in the charter.

  Two things people mix up:
    - THE METRIC is the ruler.       (e.g. accuracy, or MAE)
    - THE DEFINITION OF GOOD is the  (e.g. "beats a dumb baseline AND stops
      line you draw on that ruler.    improving")
  Your charter needs BOTH. One without the other = boss not defeated.

  Agent path: your ruler is the THREE-TEST SET.
    - known-good  (a normal request it should handle)
    - trap        (a request it should refuse or handle carefully)
    - edge        (something weird / not in the docs)
  "Good enough" = passes all three without breaking the known-good one.

================================================================================
7.0 - WAYS TO GET A GAME OVER (AND HOW TO AVOID THEM)
================================================================================

  DEATH: Over-scoping.
    You wrote a charter you can't finish in four levels.
    REVIVE: Fill in "What we are NOT doing." Cut until it fits.

  DEATH: Blank-page freeze.
    You're staring at an empty charter with no idea what to build.
    REVIVE: Do the Housing reskin (section 8.0). Start from something you know.

  DEATH: Rubber-stamp review.
    Your partner wrote "looks good" and merged. That's not a review.
    REVIVE: A real review quotes ONE specific thing and says why. Reviewing is
    graded work, not a formality.

  DEATH: Agent goes rogue.
    Your AI partner "helped" by rewriting half your project unprompted.
    REVIVE: That's what the guardrails doc is for. Tighten it. One change at a
    time (the One Change Rule -- you already know it).

================================================================================
8.0 - SECRET: NEW GAME+ (THE HOUSING RESKIN)
================================================================================

Stuck on what to build? Unlock easy on-ramp:

  Take the California Housing project. Keep the exact same shape. Swap in a
  NEW tabular dataset with a different thing to predict. Same process, new data.

This is a legit, full-credit path. You already have the muscle memory; you're
just proving you can run the process on something you didn't get handed.

================================================================================
9.0 - SAVE POINTS (WHAT TO TURN IN)
================================================================================

Commit these under module5/ before the deadline. Graded Complete / redo:

  [ ] charter.md ............ problem, path, data/tools, definition of good,
                             scope guard, roles
  [ ] issue backlog ......... 3-5 Issues framing the first working version
  [ ] agent-guardrails.md ... the rules that keep your AI partner on task
  [ ] reflection.md ......... which workflow step were you on when Housing
                             stopped? what's different this time?

  Scored on: Problem-Solving Process, Professional Communication,
  AI Partnership Quality, Critical Thinking & Ethics.

================================================================================
X.0 - CREDITS & LEGAL
================================================================================

Written by: TeachTechTerry
Escalation NPCs (real humans who can help): Mallory Milstead, Andrew Norris
Thanks to: everyone who deleted a branch and tried again

Released under the "Please Don't Sue Me" license. Print it, share it, tape it
to your monitor. Just finish your project.

REMEMBER: Level 5 is about drawing the finish line. You do not build the good
model this week. You decide what "good" means, then you go get it next level.

================================================================================
END OF FILE -- NOW GO WRITE YOUR CHARTER
================================================================================
```
