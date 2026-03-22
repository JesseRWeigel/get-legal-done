# Known LLM Legal Failure Modes

> THIS IS THE MOST IMPORTANT REFERENCE DOCUMENT IN THE ENTIRE SYSTEM.
> LLMs are UNRELIABLE for legal citations. Every single citation must be verified.
> The verifier and all agents cross-reference against these patterns.

> LEGAL DISCLAIMER: This catalog documents systematic failure patterns of LLMs
> in legal research. Use of AI for legal work requires independent verification
> of ALL output by a licensed attorney.

## CATASTROPHIC Errors (Career-Ending if Not Caught)

### L001: Hallucinated Case Citations
**Pattern**: LLM fabricates a case that does not exist — plausible-sounding case name, realistic volume/reporter/page numbers, but the case is entirely fictional.
**Frequency**: VERY HIGH — this is the single most common and dangerous LLM legal error.
**Real-world example**: Mata v. Avianca, Inc. (S.D.N.Y. 2023) — attorney sanctioned for submitting ChatGPT-generated brief with six fabricated cases.
**Guard**: EVERY citation must be verified against CourtListener, Westlaw, LexisNexis, or Google Scholar. No exceptions. Ever.

### L002: Misquoted Holdings
**Pattern**: LLM cites a real case but states its holding incorrectly — often stating a broader or narrower holding than the actual opinion, or attributing the dissent's reasoning to the majority.
**Frequency**: HIGH
**Example**: Citing Roe v. Wade for a proposition about standing when the holding was about substantive due process.
**Guard**: Every holding must be verified against the actual opinion text. Distinguish majority, concurrence, and dissent.

### L003: Citing Overruled/Reversed Cases as Good Law
**Pattern**: LLM cites a case that has been overruled, reversed, or vacated, without noting the negative history.
**Frequency**: HIGH — LLMs are trained on historical data and have no awareness of subsequent developments.
**Example**: Citing Lemon v. Kurtzman's three-part test after Kennedy v. Bremerton School District replaced it.
**Guard**: Run Shepard's/KeyCite equivalent on every case. Check for negative subsequent history.

### L004: Fabricated Statutes
**Pattern**: LLM invents a statute that does not exist — plausible title and section number, but fictional.
**Frequency**: MODERATE
**Example**: Citing "28 U.S.C. 1447(e)" when the statute only goes up to 1447(d).
**Guard**: Verify every statute citation against the actual U.S. Code or state code.

## SERIOUS Errors (Could Result in Sanctions)

### L005: Wrong Jurisdiction — Non-Binding Cited as Binding
**Pattern**: LLM cites a case from another circuit/state as if it were binding authority in the target jurisdiction.
**Frequency**: HIGH
**Example**: Citing a Ninth Circuit case as binding in the Fifth Circuit, or citing New York law in a California state court.
**Guard**: For every citation, verify: (1) which court decided it, (2) whether that court's decisions are binding in our jurisdiction.

### L006: Outdated Statutes
**Pattern**: LLM cites a version of a statute that has been amended, repealed, or recodified.
**Frequency**: MODERATE
**Example**: Citing a pre-2017 version of the tax code after the Tax Cuts and Jobs Act.
**Guard**: Check the effective date and amendment history of every statute.

### L007: Incorrect Standard of Review
**Pattern**: LLM applies the wrong standard of review for the procedural posture.
**Frequency**: MODERATE
**Example**: Applying de novo review to factual findings (should be clearly erroneous), or applying abuse of discretion to questions of law (should be de novo).
**Guard**: Verify the standard of review against the specific procedural posture and type of issue.

### L008: Mixed-Up Parties
**Pattern**: LLM confuses plaintiff and defendant, appellant and appellee, or attributes arguments/positions to the wrong party.
**Frequency**: MODERATE
**Example**: Stating "the defendant argued..." when it was actually the plaintiff's argument.
**Guard**: Track party designations carefully. Verify which party made which argument.

## MODERATE Errors (Embarrassing, Potentially Harmful)

### L009: Fake or Incorrect Dates
**Pattern**: LLM assigns wrong dates to cases, statutes, or events.
**Frequency**: MODERATE
**Example**: Stating a case was decided in 2019 when it was actually decided in 2009.
**Guard**: Verify dates against the actual source.

### L010: Confusing Concurrence/Dissent with Majority
**Pattern**: LLM attributes reasoning from a concurrence or dissent to the majority opinion.
**Frequency**: MODERATE
**Example**: Citing Justice Thomas's concurrence in Dobbs as the holding of the Court.
**Guard**: Verify which opinion the cited language comes from.

### L011: Citing Dicta as Holding
**Pattern**: LLM treats obiter dictum (incidental remarks) as the holding of the case.
**Frequency**: HIGH
**Example**: Treating a court's hypothetical discussion as a binding rule.
**Guard**: Distinguish holding (necessary to the outcome) from dicta (everything else).

### L012: Incorrect Procedural History
**Pattern**: LLM misstates the procedural history of a case — wrong lower court, wrong procedural posture, wrong disposition.
**Frequency**: MODERATE
**Guard**: Verify procedural history against the actual opinion.

### L013: Conflating Similar but Distinct Legal Standards
**Pattern**: LLM treats different legal standards as interchangeable.
**Frequency**: HIGH
**Example**: Conflating "preponderance of the evidence" with "clear and convincing evidence," or confusing "rational basis" with "intermediate scrutiny."
**Guard**: State the precise legal standard and cite the authority for it.

### L014: Misapplying Multi-Factor Tests
**Pattern**: LLM states a multi-factor test but applies the wrong number of factors, wrong factors, or misweights them.
**Frequency**: MODERATE
**Example**: Stating the Daubert test has four factors when the court identified a non-exhaustive list, or applying the wrong factors for a preliminary injunction analysis.
**Guard**: Quote the exact test from the controlling authority.

### L015: Fabricated Quotations
**Pattern**: LLM generates a plausible-sounding quote and attributes it to a real case, but the quote is fabricated.
**Frequency**: MODERATE-HIGH
**Guard**: Every direct quote must be verified against the actual source text. If you cannot verify the quote, paraphrase instead and note that the exact language should be verified.

## How to Use This Catalog

1. **Researcher**: Before searching, know which errors are most likely for this type of research. Add verification steps.
2. **Executor**: Consult relevant entries when performing analysis. Follow guards. Flag any uncertainty.
3. **Verifier**: After execution, cross-reference EVERY citation against L001-L004 (existence checks) and L005-L008 (accuracy checks). These checks are NON-NEGOTIABLE.
4. **Planner**: Build verification tasks into every plan. Never plan a phase without a verification step.
5. **All agents**: When in doubt, say "I cannot verify this citation" rather than presenting an unverified citation as fact.
