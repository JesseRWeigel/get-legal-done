---
name: new-project
description: Initialize a new legal research project
---

<process>

## Initialize New Legal Research Project

LEGAL DISCLAIMER: This tool assists with legal research. It is not a substitute for licensed legal counsel. All output must be independently verified by a licensed attorney.

### Step 1: Create project structure
Create the `.gld/` directory and all required subdirectories:
- `.gld/` — project state and config
- `.gld/observability/sessions/` — session logs
- `.gld/traces/` — execution traces
- `knowledge/` — research knowledge base
- `briefs/` — output documents
- `.scratch/` — temporary working files (gitignored)

### Step 2: Gather project information
Ask the user:
1. **Project name**: What is this legal matter about?
2. **Legal question**: What specific legal question are you researching?
3. **Jurisdiction**: Which court/jurisdiction? (federal circuit, state court, etc.)
4. **Document type**: What is the final deliverable? (brief, memo, motion, research memo)
5. **Model profile**: litigation (default), research-memo, due-diligence, brief-writing, or quick-research?
6. **Research mode**: explore, balanced (default), exploit, or adaptive?

### Step 3: Create initial ROADMAP.md
Based on the legal question, create a phase breakdown:

```markdown
# [Project Name] -- Roadmap

## Phase 1: Issue Identification
**Goal**: Identify all legal issues arising from the fact pattern

## Phase 2: Jurisdiction and Procedural Posture
**Goal**: Determine jurisdiction, governing law, standard of review, and procedural requirements

## Phase 3: Case Law Research
**Goal**: Find binding and persuasive authority on each issue

## Phase 4: Statutory and Regulatory Research
**Goal**: Identify and analyze applicable statutes, regulations, and rules

## Phase 5: Legal Analysis
**Goal**: Construct IRAC/CREAC analysis for each issue

## Phase 6: Brief / Document Drafting
**Goal**: Draft the final legal document with proper citations
```

Adjust phases based on the specific matter. Some projects need more phases (e.g., constitutional analysis, multi-jurisdictional survey), some need fewer.

### Step 4: Initialize state
Create STATE.md and state.json with:
- Project name and creation date
- Phase listing from ROADMAP
- Phase 1 set as active
- Research mode and autonomy mode

### Step 5: Initialize config
Create `.gld/config.json` with user's choices.

### Step 6: Initialize git
If not already a git repo, initialize one. Add `.scratch/` to `.gitignore`.
Commit the initial project structure.

### Step 7: Convention prompting
Ask if the user wants to pre-set any conventions:
- Jurisdiction (federal/state, specific court)
- Governing law
- Citation format (Bluebook, ALWD, local rules)
- Procedural posture
- Cause of action / legal theory

Lock any conventions the user specifies.

### Step 8: Summary
Display:
- Project structure created
- Phases from roadmap
- Active conventions
- Next step: run `plan-phase` to begin Phase 1

</process>
