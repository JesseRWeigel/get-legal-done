# Get Legal Done

> An AI copilot for autonomous legal research and brief writing — from legal question to verified, citation-accurate memoranda and briefs.

**Inspired by [Get Physics Done](https://github.com/psi-oss/get-physics-done)** — the open-source AI copilot that autonomously conducts physics research. Get Legal Done adapts GPD's architecture for legal research, where citation accuracy and analytical rigor are paramount.

## Vision

LLM hallucination of legal citations is the #1 failure mode in AI-assisted legal work — lawyers have been sanctioned for submitting AI-generated briefs with fabricated case citations. Get Legal Done treats this as its core design constraint: every citation is verified, every holding is checked, every standard of review is locked.

Get Legal Done wraps LLM capabilities in a verification-first framework that:
- **Locks jurisdictional parameters** across phases (jurisdiction, governing law, standard of review, burden of proof, citation format)
- **Verifies every citation** against real legal databases (case existence, holding accuracy, subsequent history, good law status)
- **Decomposes research** into phases: issue identification → jurisdiction/standard determination → case law research → statutory research → analysis → brief/memo writing
- **Runs adversarial review** — referee panel examines arguments from plaintiff, defendant, and judicial perspectives

## Architecture

Adapted from GPD's three-layer design:

### Layer 1 — Core Library (Python)
State management, phase lifecycle, git operations, convention locks, verification kernel.

### Layer 2 — MCP Servers
- `gld-state` — Project state queries
- `gld-conventions` — Jurisdictional and analytical framework locks
- `gld-protocols` — Legal research methodology protocols (case law analysis, statutory interpretation, regulatory research, constitutional analysis)
- `gld-patterns` — Cross-project learned patterns
- `gld-verification` — Citation verification and analytical rigor checks
- `gld-errors` — Known LLM legal failure modes (hallucinated citations, misquoted holdings, outdated law)

### Layer 3 — Agents & Commands
- `gld-planner` — Issue spotting and research task decomposition
- `gld-executor` — Primary research and analysis execution
- `gld-verifier` — Citation verification and analytical rigor checking
- `gld-researcher` — Case law, statutory, and regulatory research
- `gld-analyst` — Legal analysis and argument construction
- `gld-paper-writer` — Brief, memorandum, and motion drafting
- `gld-referee` — Multi-perspective adversarial review (plaintiff/defendant/court)

## Convention Lock Fields

Legal-specific framework consistency:
1. Jurisdiction (federal/state, circuit, district)
2. Governing law (state law choice, federal preemption status)
3. Standard of review (de novo, abuse of discretion, clearly erroneous, rational basis, strict scrutiny)
4. Burden of proof (preponderance, clear and convincing, beyond reasonable doubt)
5. Citation format (Bluebook, ALWD, court-specific local rules)
6. Procedural posture (motion to dismiss, summary judgment, trial, appeal)
7. Cause of action / legal theory
8. Statute of limitations framework
9. Damages theory (compensatory, punitive, equitable)
10. Key definitions (terms of art with jurisdiction-specific meanings)

## Verification Framework

1. **Citation existence** — every cited case, statute, and regulation exists
2. **Holding accuracy** — quoted or paraphrased holdings match the actual opinion
3. **Subsequent history** — cases not reversed, overruled, or distinguished on the cited point
4. **Good law status** — cited authority still valid (not superseded by statute/later case)
5. **Standard of review correctness** — correct standard applied for procedural posture
6. **Jurisdictional accuracy** — cited authority is binding or properly identified as persuasive
7. **Statutory currency** — statutes cited in current version, amendments noted
8. **Quotation accuracy** — direct quotes match source text exactly
9. **Logical validity** — legal reasoning follows from premises, no circular arguments
10. **Completeness** — adverse authority addressed, not ignored
11. **Format compliance** — citations conform to Bluebook/ALWD/local rules
12. **Ethical compliance** — arguments not frivolous, candor to tribunal maintained

## Important Disclaimer

**Get Legal Done is a research and drafting tool, not a substitute for licensed legal counsel.** All output must be reviewed by a licensed attorney before use in any legal proceeding. This tool does not provide legal advice.

## Status

**Early development** — Building core infrastructure. Contributions welcome!

## Relationship to GPD

This project reuses GPD's domain-agnostic infrastructure and replaces physics-specific components with legal research methodology. The referee panel pattern maps naturally to adversarial legal analysis.

We plan to showcase this in the [GPD Discussion Show & Tell](https://github.com/psi-oss/get-physics-done/discussions) once operational.

## Getting Started

```bash
# Coming soon
npx get-legal-done
```

## Contributing

We're looking for contributors with:
- Legal research experience (any jurisdiction)
- Legal technology / legal AI experience
- Familiarity with Bluebook citation, legal databases (Westlaw, LexisNexis, CourtListener)
- Familiarity with GPD's architecture

See the [Issues](../../issues) for specific tasks.

## License

MIT
