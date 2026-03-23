# Intellectual Property Protocols

> Step-by-step methodology guides for patent, copyright, and trademark analysis.

## Protocol: Patent Validity Analysis

### When to Use
Evaluating whether a patent claim meets the statutory requirements for patentability under 35 U.S.C.

### Steps
1. **Identify the claim type** — utility patent, design patent, or plant patent; identify independent vs dependent claims
2. **Assess patentable subject matter (§ 101)** — apply the Alice/Mayo two-step: (1) Is the claim directed to an abstract idea, law of nature, or natural phenomenon? (2) If yes, does the claim recite an inventive concept that transforms it into something significantly more?
3. **Assess novelty (§ 102)** — is every element of the claim found in a single prior art reference? Check patents, publications, public use, on sale, or otherwise available to the public before the effective filing date
4. **Assess nonobviousness (§ 103)** — apply the Graham v. John Deere framework: (a) scope and content of prior art, (b) differences between prior art and the claims, (c) level of ordinary skill in the art, (d) secondary considerations (commercial success, long-felt need, failure of others, copying, teaching away)
5. **Assess enablement and written description (§ 112)** — does the specification enable a person of ordinary skill to make and use the invention without undue experimentation? Is the invention described in sufficient detail to show the inventor had possession?
6. **Check for indefiniteness (§ 112)** — are the claims sufficiently clear to inform those skilled in the art of the scope of the invention with reasonable certainty? (Nautilus v. Biosig)
7. **State the conclusion** — the claim is valid/invalid, identifying the weakest requirement

### Common LLM Pitfalls
- Applying the pre-AIA first-to-invent rules instead of the post-AIA (2013) first-inventor-to-file system
- Conflating novelty (§ 102, single reference) with nonobviousness (§ 103, combination of references)
- Treating Alice/Mayo § 101 analysis as a simple categorization instead of a two-step test
- Ignoring secondary considerations of nonobviousness (they can overcome a prima facie case)

---

## Protocol: Patent Infringement Analysis

### When to Use
Determining whether an accused product or method infringes a patent claim.

### Steps
1. **Construe the claims** — determine the meaning of each claim term using intrinsic evidence (claim language, specification, prosecution history) and, if necessary, extrinsic evidence (dictionaries, expert testimony); apply Phillips v. AWH framework
2. **Assess literal infringement** — does the accused product/method meet every limitation of at least one claim? (All-elements rule: every element must be present)
3. **If no literal infringement, assess the doctrine of equivalents** — for each unmet limitation, is there an equivalent in the accused product that performs substantially the same function, in substantially the same way, to achieve substantially the same result? (function-way-result test)
4. **Check prosecution history estoppel** — was the claim limitation narrowed during prosecution? If so, the patentee may be estopped from recapturing the surrendered scope through equivalents (Festo)
5. **Assess infringement type** — direct (§ 271(a)), induced (§ 271(b), requires knowledge and intent), or contributory (§ 271(c), selling a component with no substantial non-infringing use)
6. **Check for defenses** — invalidity, experimental use, prior user rights (§ 273), exhaustion, license, laches/estoppel
7. **State the conclusion** — the accused product does/does not infringe claim X, literally or under the doctrine of equivalents

### Common LLM Pitfalls
- Applying the doctrine of equivalents without first performing a claim-by-claim, limitation-by-limitation analysis
- Forgetting prosecution history estoppel when the claim was amended during prosecution
- Confusing direct infringement with induced or contributory infringement (different intent requirements)
- Construing claims based on the accused product rather than on the intrinsic record

---

## Protocol: Copyright Analysis

### When to Use
Evaluating copyright subsistence, ownership, infringement, or fair use defenses.

### Steps
1. **Confirm copyrightable subject matter** — original work of authorship fixed in a tangible medium of expression (17 U.S.C. § 102); does not protect ideas, procedures, systems, or methods of operation (§ 102(b), Baker v. Selden)
2. **Assess originality** — independent creation plus minimal creativity (Feist); facts and short phrases are generally not copyrightable
3. **Identify the copyright owner** — author, employer under work-for-hire doctrine (§ 101, § 201(b)), or assignee
4. **Assess infringement** — (a) did the defendant actually copy? (access + probative similarity), and (b) is the copying actionable? (substantial similarity of protected expression to an ordinary observer)
5. **Apply the idea-expression dichotomy** — filter out unprotectable elements: ideas, facts, scenes-a-faire, merger doctrine (when an idea can be expressed in only one way, the expression merges with the idea and is not protected)
6. **Evaluate fair use (§ 107)** — four factors: (1) purpose and character of use (commercial vs nonprofit, transformative use — Andy Warhol Foundation v. Goldsmith, 2023), (2) nature of the copyrighted work, (3) amount and substantiality used, (4) effect on the market for the original
7. **State the conclusion** — infringement is/is not established; fair use does/does not apply

### Common LLM Pitfalls
- Treating fair use as a bright-line rule rather than a case-by-case balancing test
- Applying pre-Warhol Foundation transformativeness analysis without accounting for the 2023 Supreme Court narrowing
- Confusing copyright protection for expression with protection for ideas or facts
- Assuming registration is required for copyright to exist (registration is required to file suit, but copyright attaches upon fixation)

---

## Protocol: Trademark Analysis

### When to Use
Evaluating trademark validity, registrability, infringement, or dilution claims.

### Steps
1. **Classify the mark on the distinctiveness spectrum** — generic (never protectable), descriptive (protectable only with secondary meaning), suggestive, arbitrary, or fanciful (inherently distinctive)
2. **Assess use in commerce** — is the mark used in connection with goods or services in interstate commerce? (use is the basis of trademark rights in the US)
3. **Assess likelihood of confusion** — apply the multi-factor test (varies by circuit; e.g., Polaroid factors in 2d Cir., Sleekcraft factors in 9th Cir.): similarity of marks, relatedness of goods, strength of the senior mark, evidence of actual confusion, marketing channels, consumer sophistication, intent
4. **Evaluate defenses** — fair use (descriptive fair use, nominative fair use), first sale/exhaustion, parody, laches, acquiescence, genericization
5. **For dilution claims (§ 43(c))** — only available for famous marks; assess dilution by blurring (association that impairs distinctiveness) or dilution by tarnishment (association that harms reputation)
6. **Check registrability bars** — immoral or scandalous matter, deceptive marks, primarily merely a surname, functional features, geographic marks
7. **State the conclusion** — the mark is valid/invalid; infringement/dilution is/is not likely

### Common LLM Pitfalls
- Confusing trademark infringement (likelihood of confusion) with dilution (no confusion required, but mark must be famous)
- Treating descriptive marks as inherently protectable without analyzing secondary meaning
- Applying a single circuit's likelihood-of-confusion factors universally without identifying the applicable circuit
- Forgetting that functionality is an absolute bar to trademark protection regardless of distinctiveness
