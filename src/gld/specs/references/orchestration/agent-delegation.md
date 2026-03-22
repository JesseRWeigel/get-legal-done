# Agent Delegation Protocol

> How the orchestrator spawns subagents, collects results, and handles failures.

## Task Delegation Pattern

```
orchestrator
  |-- spawn(gld-researcher, {phase_goal})  -> RESEARCH.md
  |-- spawn(gld-planner, {research, phase_goal})  -> PLAN.md
  |-- for each wave:
  |   |-- spawn(gld-executor, {task_1})  -> artifacts + SUMMARY
  |   |-- spawn(gld-executor, {task_2})  -> artifacts + SUMMARY  (parallel)
  |   +-- verify_artifacts_on_disk()
  |-- spawn(gld-analyst, {research, facts})  -> ANALYSIS.md
  |-- spawn(gld-verifier, {phase_artifacts})  -> VERIFICATION-REPORT.md  [NON-NEGOTIABLE]
  |   +-- if FAIL: create gap-closure plans, re-execute
  |-- spawn(gld-paper-writer, {analysis, research})  -> briefs/
  |-- spawn(gld-referee, {brief})  -> REVIEW-REPORT.md
  +-- update STATE.md
```

## Artifact Recovery Protocol

**CRITICAL**: Never trust that a subagent's reported success means files were written.

After every subagent returns:
1. Parse the `gld_return` envelope from SUMMARY.md
2. Verify every file in `files_written` exists on disk
3. If missing: attempt to extract content from the agent's response text
4. If still missing: log error and flag for re-execution

## Citation Verification Protocol

**EVEN MORE CRITICAL**: Never trust that a subagent's citations are real.

After every research/analysis subagent returns:
1. Extract all citations from output files
2. Cross-reference against the LLM error catalog (L001-L015)
3. Flag all citations for verification by gld-verifier
4. Do NOT proceed to brief writing until verification completes

## Return Envelope Parsing

Every subagent MUST produce a `gld_return:` YAML block in their SUMMARY.md:

```yaml
gld_return:
  status: completed | checkpoint | blocked | failed
  files_written: [...]
  files_modified: [...]
  issues: [...]
  next_actions: [...]
  claims_supported: [...]
  citations_verified: [...]
  citations_flagged: [...]
  conventions_proposed: {field: value}
  verification_evidence: {...}
```

The orchestrator uses this structured data -- NOT the agent's prose -- to determine:
- Whether to proceed to the next wave
- What files to verify
- What convention proposals to evaluate
- What verification evidence to feed to the verifier
- What citations need independent verification

## Failure Handling

| Agent Status | Orchestrator Action |
|-------------|-------------------|
| `completed` | Verify artifacts AND citations, proceed |
| `checkpoint` | Save state, can resume later |
| `blocked` | Analyze blocker, may route to different agent |
| `failed` | Analyze failure, create targeted re-execution plan |

### Citation-Specific Failure Handling

| Citation Issue | Action |
|---------------|--------|
| Hallucinated citation (L001) | REMOVE immediately, flag for replacement |
| Inaccurate holding (L002) | Route back to executor with actual opinion |
| Overruled case (L003) | Route to researcher for current authority |
| Fabricated statute (L004) | REMOVE immediately, verify correct citation |
| Wrong jurisdiction (L005) | Route to researcher with correct jurisdiction |

## Context Budget

Each subagent gets a fresh context window. The orchestrator targets ~15% of its own context for coordination. Budget allocation per phase type:

| Phase Type | Orchestrator | Planner | Executor | Verifier | Researcher |
|-----------|-------------|---------|----------|----------|------------|
| Issue identification | 10% | 10% | 50% | 15% | 15% |
| Case law research | 10% | 5% | 50% | 20% | 15% |
| Legal analysis | 15% | 10% | 50% | 25% | -- |
| Brief writing | 10% | 5% | 60% | 15% | 10% |
| Verification | 10% | -- | -- | 80% | 10% |
