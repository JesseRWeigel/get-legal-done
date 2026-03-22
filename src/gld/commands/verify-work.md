---
name: verify-work
description: Run the 12-check legal verification framework
---

<process>

## Verify Work

THIS IS THE MOST IMPORTANT COMMAND IN THE SYSTEM. Legal citations must be verified.

### Overview
Run post-hoc verification on completed phase work using the 12-check framework.

### Step 1: Collect Artifacts
Gather all output from the current phase:
- Research memos and case summaries
- Legal analysis documents
- Brief/motion drafts
- Citation appendices

### Step 2: Extract All Citations
Parse every citation from every document:
- Case citations (e.g., Brown v. Board of Education, 347 U.S. 483 (1954))
- Statute citations (e.g., 42 U.S.C. 1983)
- Regulation citations (e.g., 29 C.F.R. 1630.2)
- Secondary source citations

### Step 3: Build Evidence Registry
Extract verification evidence from artifacts:
- All citations with their claimed holdings
- All direct quotes with their sources
- Authority classifications (binding/persuasive)
- Adverse authority identified
- IRAC/CREAC reasoning steps

### Step 4: Run Verification
Spawn gld-verifier with:
- All phase artifacts
- Evidence registry
- Convention locks
- LLM error catalog

### Step 5: Process Verdict
Parse the VERIFICATION-REPORT.md:
- If PASS: record in state, proceed
- If PARTIAL: create targeted gap-closure for MAJOR failures
- If FAIL: create gap-closure for CRITICAL failures, block downstream
  - HALLUCINATED CITATIONS: Remove immediately, flag for replacement
  - INACCURATE HOLDINGS: Flag for correction
  - BAD LAW: Flag for replacement with current authority

### Step 6: Route Failures
For each failure, route to the appropriate agent:
- Hallucinated citations — gld-researcher (find real authority)
- Inaccurate holdings — gld-executor (re-read opinion, correct)
- Bad law — gld-researcher (find current authority)
- Adverse authority gaps — gld-researcher (adverse authority search)
- Format errors — gld-paper-writer (citation format correction)
- Ethical issues — STOP and flag to user immediately

### Step 7: Update State
Record verification results in STATE.md:
- Verdict hash (content-addressed)
- Pass/fail counts
- Any unresolved issues
- Citation verification summary

</process>
