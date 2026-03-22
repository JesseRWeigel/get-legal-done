"""Content-addressed verification kernel for legal research.

Runs predicates over evidence registries and produces SHA-256 verdicts.
Adapted from GPD's kernel.py for legal citation and analysis verification.

THIS IS THE MOST CRITICAL COMPONENT. LLMs routinely hallucinate legal
citations, misstate holdings, and cite overruled cases. The verification
kernel is the primary defense against these catastrophic errors.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable

from .constants import VERIFICATION_CHECKS, SEVERITY_CRITICAL, SEVERITY_MAJOR, SEVERITY_MINOR, SEVERITY_NOTE


class Severity(str, Enum):
    CRITICAL = SEVERITY_CRITICAL
    MAJOR = SEVERITY_MAJOR
    MINOR = SEVERITY_MINOR
    NOTE = SEVERITY_NOTE


@dataclass
class CheckResult:
    """Result of a single verification check."""

    check_id: str
    name: str
    status: str  # PASS | FAIL | SKIP | WARN
    severity: Severity
    message: str = ""
    evidence: dict[str, Any] = field(default_factory=dict)
    suggestions: list[str] = field(default_factory=list)


@dataclass
class Verdict:
    """Complete verification verdict with content-addressed hashes."""

    registry_hash: str
    predicates_hash: str
    verdict_hash: str
    overall: str  # PASS | FAIL | PARTIAL
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    results: dict[str, CheckResult] = field(default_factory=dict)
    summary: str = ""

    @property
    def critical_failures(self) -> list[CheckResult]:
        return [
            r
            for r in self.results.values()
            if r.status == "FAIL" and r.severity == Severity.CRITICAL
        ]

    @property
    def major_failures(self) -> list[CheckResult]:
        return [
            r
            for r in self.results.values()
            if r.status == "FAIL" and r.severity == Severity.MAJOR
        ]

    @property
    def all_failures(self) -> list[CheckResult]:
        return [r for r in self.results.values() if r.status == "FAIL"]

    @property
    def pass_count(self) -> int:
        return sum(1 for r in self.results.values() if r.status == "PASS")

    @property
    def fail_count(self) -> int:
        return sum(1 for r in self.results.values() if r.status == "FAIL")

    def to_dict(self) -> dict[str, Any]:
        return {
            "registry_hash": self.registry_hash,
            "predicates_hash": self.predicates_hash,
            "verdict_hash": self.verdict_hash,
            "overall": self.overall,
            "timestamp": self.timestamp,
            "summary": self.summary,
            "results": {
                k: {
                    "check_id": v.check_id,
                    "name": v.name,
                    "status": v.status,
                    "severity": v.severity.value,
                    "message": v.message,
                    "evidence": v.evidence,
                    "suggestions": v.suggestions,
                }
                for k, v in self.results.items()
            },
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


# -- Predicate Type -----------------------------------------------------------

# A predicate takes an evidence registry and returns a CheckResult
Predicate = Callable[[dict[str, Any]], CheckResult]


# -- Built-in Legal Predicates ------------------------------------------------

def check_citation_existence(evidence: dict[str, Any]) -> CheckResult:
    """Check that every cited case/statute/regulation actually exists."""
    citations = evidence.get("citations", [])
    verified_citations = evidence.get("verified_citations", [])
    unverified_citations = evidence.get("unverified_citations", [])
    hallucinated_citations = evidence.get("hallucinated_citations", [])

    if not citations:
        return CheckResult(
            check_id="citation_existence",
            name="Citation Existence",
            status="SKIP",
            severity=Severity.CRITICAL,
            message="No citations provided for verification.",
        )

    if hallucinated_citations:
        return CheckResult(
            check_id="citation_existence",
            name="Citation Existence",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"Found {len(hallucinated_citations)} citation(s) that do not exist in any database.",
            evidence={"hallucinated": hallucinated_citations},
            suggestions=[
                f"Remove or replace hallucinated citation: {c}" for c in hallucinated_citations[:5]
            ],
        )

    if unverified_citations:
        return CheckResult(
            check_id="citation_existence",
            name="Citation Existence",
            status="WARN",
            severity=Severity.CRITICAL,
            message=f"{len(unverified_citations)} citation(s) could not be verified (may still exist).",
            evidence={"unverified": unverified_citations},
            suggestions=["Manually verify these citations against Westlaw, LexisNexis, or CourtListener."],
        )

    return CheckResult(
        check_id="citation_existence",
        name="Citation Existence",
        status="PASS",
        severity=Severity.CRITICAL,
        message=f"All {len(citations)} citation(s) verified to exist.",
    )


def check_holding_accuracy(evidence: dict[str, Any]) -> CheckResult:
    """Check that stated holdings match actual judicial opinions."""
    holdings_claimed = evidence.get("holdings_claimed", [])
    holdings_verified = evidence.get("holdings_verified", [])
    holdings_inaccurate = evidence.get("holdings_inaccurate", [])

    if not holdings_claimed:
        return CheckResult(
            check_id="holding_accuracy",
            name="Holding Accuracy",
            status="SKIP",
            severity=Severity.CRITICAL,
            message="No holdings claimed for verification.",
        )

    if holdings_inaccurate:
        return CheckResult(
            check_id="holding_accuracy",
            name="Holding Accuracy",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"{len(holdings_inaccurate)} holding(s) do not match the actual opinion.",
            evidence={"inaccurate": holdings_inaccurate},
            suggestions=[
                "Re-read the actual opinion and correct the stated holding.",
                "Distinguish between holding, dicta, and concurrence/dissent.",
            ],
        )

    return CheckResult(
        check_id="holding_accuracy",
        name="Holding Accuracy",
        status="PASS",
        severity=Severity.CRITICAL,
        message=f"All {len(holdings_claimed)} holding(s) verified against opinions.",
    )


def check_subsequent_history(evidence: dict[str, Any]) -> CheckResult:
    """Check that cited cases have not been reversed, vacated, or overruled."""
    cases_checked = evidence.get("cases_shepardized", [])
    negative_history = evidence.get("negative_history", [])

    if not cases_checked:
        return CheckResult(
            check_id="subsequent_history",
            name="Subsequent History",
            status="WARN",
            severity=Severity.CRITICAL,
            message="No cases checked for subsequent history (Shepardize/KeyCite).",
            suggestions=["Run all cited cases through Shepard's or KeyCite before relying on them."],
        )

    if negative_history:
        return CheckResult(
            check_id="subsequent_history",
            name="Subsequent History",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"{len(negative_history)} case(s) have negative subsequent history.",
            evidence={"negative_history": negative_history},
            suggestions=[
                "Do not cite reversed/overruled cases as binding authority.",
                "If citing for historical context, note the negative history explicitly.",
            ],
        )

    return CheckResult(
        check_id="subsequent_history",
        name="Subsequent History",
        status="PASS",
        severity=Severity.CRITICAL,
        message=f"All {len(cases_checked)} case(s) checked -- no negative history.",
    )


def check_good_law_status(evidence: dict[str, Any]) -> CheckResult:
    """Check that all cited authority is still good law."""
    authorities_checked = evidence.get("authorities_checked", [])
    bad_law = evidence.get("bad_law", [])
    superseded_statutes = evidence.get("superseded_statutes", [])

    issues = bad_law + superseded_statutes

    if not authorities_checked:
        return CheckResult(
            check_id="good_law_status",
            name="Good Law Status",
            status="WARN",
            severity=Severity.CRITICAL,
            message="No authorities checked for current validity.",
            suggestions=["Verify all cited authorities are still good law."],
        )

    if issues:
        return CheckResult(
            check_id="good_law_status",
            name="Good Law Status",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"{len(issues)} authority/ies no longer good law.",
            evidence={"bad_law": bad_law, "superseded": superseded_statutes},
        )

    return CheckResult(
        check_id="good_law_status",
        name="Good Law Status",
        status="PASS",
        severity=Severity.CRITICAL,
        message=f"All {len(authorities_checked)} authorities confirmed as good law.",
    )


def check_standard_of_review(evidence: dict[str, Any]) -> CheckResult:
    """Check correct standard of review is applied."""
    claimed_standard = evidence.get("claimed_standard", "")
    correct_standard = evidence.get("correct_standard", "")
    procedural_posture = evidence.get("procedural_posture", "")

    if not claimed_standard:
        return CheckResult(
            check_id="standard_of_review",
            name="Standard of Review",
            status="WARN",
            severity=Severity.MAJOR,
            message="No standard of review specified.",
            suggestions=["Identify and state the applicable standard of review."],
        )

    if correct_standard and claimed_standard != correct_standard:
        return CheckResult(
            check_id="standard_of_review",
            name="Standard of Review",
            status="FAIL",
            severity=Severity.MAJOR,
            message=f"Incorrect standard: claimed '{claimed_standard}', should be '{correct_standard}'.",
            evidence={"claimed": claimed_standard, "correct": correct_standard, "posture": procedural_posture},
        )

    return CheckResult(
        check_id="standard_of_review",
        name="Standard of Review",
        status="PASS",
        severity=Severity.MAJOR,
        message=f"Standard of review '{claimed_standard}' is correct for this procedural posture.",
    )


def check_jurisdictional_accuracy(evidence: dict[str, Any]) -> CheckResult:
    """Check binding vs persuasive authority is correctly identified."""
    authority_classifications = evidence.get("authority_classifications", [])
    misclassified = evidence.get("misclassified_authority", [])

    if not authority_classifications:
        return CheckResult(
            check_id="jurisdictional_accuracy",
            name="Jurisdictional Accuracy",
            status="WARN",
            severity=Severity.MAJOR,
            message="No authority classified as binding vs persuasive.",
            suggestions=["Classify each cited authority as binding or persuasive for this jurisdiction."],
        )

    if misclassified:
        return CheckResult(
            check_id="jurisdictional_accuracy",
            name="Jurisdictional Accuracy",
            status="FAIL",
            severity=Severity.MAJOR,
            message=f"{len(misclassified)} authority/ies misclassified (binding/persuasive).",
            evidence={"misclassified": misclassified},
            suggestions=[
                "Verify the court hierarchy for the target jurisdiction.",
                "Only same-jurisdiction, higher-court decisions are binding.",
            ],
        )

    return CheckResult(
        check_id="jurisdictional_accuracy",
        name="Jurisdictional Accuracy",
        status="PASS",
        severity=Severity.MAJOR,
        message=f"All {len(authority_classifications)} authority classifications are correct.",
    )


def check_statutory_currency(evidence: dict[str, Any]) -> CheckResult:
    """Check that cited statutes are the current version."""
    statutes_cited = evidence.get("statutes_cited", [])
    outdated_statutes = evidence.get("outdated_statutes", [])

    if not statutes_cited:
        return CheckResult(
            check_id="statutory_currency",
            name="Statutory Currency",
            status="SKIP",
            severity=Severity.MAJOR,
            message="No statutes cited.",
        )

    if outdated_statutes:
        return CheckResult(
            check_id="statutory_currency",
            name="Statutory Currency",
            status="FAIL",
            severity=Severity.MAJOR,
            message=f"{len(outdated_statutes)} statute(s) are not the current version.",
            evidence={"outdated": outdated_statutes},
            suggestions=["Update statute citations to reflect current codification."],
        )

    return CheckResult(
        check_id="statutory_currency",
        name="Statutory Currency",
        status="PASS",
        severity=Severity.MAJOR,
        message=f"All {len(statutes_cited)} statute citation(s) are current.",
    )


def check_quotation_accuracy(evidence: dict[str, Any]) -> CheckResult:
    """Check that direct quotes match source material exactly."""
    quotes = evidence.get("quotes", [])
    inaccurate_quotes = evidence.get("inaccurate_quotes", [])

    if not quotes:
        return CheckResult(
            check_id="quotation_accuracy",
            name="Quotation Accuracy",
            status="SKIP",
            severity=Severity.MAJOR,
            message="No direct quotes to verify.",
        )

    if inaccurate_quotes:
        return CheckResult(
            check_id="quotation_accuracy",
            name="Quotation Accuracy",
            status="FAIL",
            severity=Severity.MAJOR,
            message=f"{len(inaccurate_quotes)} quote(s) do not match source material.",
            evidence={"inaccurate": inaccurate_quotes},
            suggestions=[
                "Verify all quotes against the original source.",
                "Use proper ellipsis and bracket notation for alterations.",
            ],
        )

    return CheckResult(
        check_id="quotation_accuracy",
        name="Quotation Accuracy",
        status="PASS",
        severity=Severity.MAJOR,
        message=f"All {len(quotes)} direct quote(s) verified against sources.",
    )


def check_logical_validity(evidence: dict[str, Any]) -> CheckResult:
    """Check that legal reasoning is sound (IRAC/CREAC structure)."""
    reasoning_steps = evidence.get("reasoning_steps", [])
    logical_gaps = evidence.get("logical_gaps", [])
    irac_complete = evidence.get("irac_complete", False)

    if not reasoning_steps:
        return CheckResult(
            check_id="logical_validity",
            name="Logical Validity",
            status="SKIP",
            severity=Severity.MAJOR,
            message="No reasoning steps provided for verification.",
        )

    if logical_gaps:
        return CheckResult(
            check_id="logical_validity",
            name="Logical Validity",
            status="FAIL",
            severity=Severity.MAJOR,
            message=f"Found {len(logical_gaps)} gap(s) in legal reasoning.",
            evidence={"gaps": logical_gaps},
            suggestions=[f"Address reasoning gap: {g}" for g in logical_gaps[:5]],
        )

    return CheckResult(
        check_id="logical_validity",
        name="Logical Validity",
        status="PASS",
        severity=Severity.MAJOR,
        message=f"Legal reasoning verified across {len(reasoning_steps)} step(s).",
    )


def check_completeness(evidence: dict[str, Any]) -> CheckResult:
    """Check that adverse authority is addressed (Model Rule 3.3 compliance)."""
    adverse_authority = evidence.get("adverse_authority_identified", [])
    adverse_authority_addressed = evidence.get("adverse_authority_addressed", [])
    counterarguments_addressed = evidence.get("counterarguments_addressed", [])

    unaddressed = [a for a in adverse_authority if a not in adverse_authority_addressed]

    if unaddressed:
        return CheckResult(
            check_id="completeness",
            name="Completeness (Adverse Authority)",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"{len(unaddressed)} adverse authority/ies not addressed (Rule 3.3 risk).",
            evidence={"unaddressed": unaddressed},
            suggestions=[
                "Model Rule 3.3(a)(2) requires disclosure of directly adverse authority.",
                "Address each adverse authority with distinguishing arguments.",
            ],
        )

    if not adverse_authority:
        return CheckResult(
            check_id="completeness",
            name="Completeness (Adverse Authority)",
            status="WARN",
            severity=Severity.CRITICAL,
            message="No adverse authority search conducted.",
            suggestions=[
                "Search for authority opposing your position.",
                "Failure to disclose adverse authority violates Model Rule 3.3(a)(2).",
            ],
        )

    return CheckResult(
        check_id="completeness",
        name="Completeness (Adverse Authority)",
        status="PASS",
        severity=Severity.CRITICAL,
        message=f"All {len(adverse_authority)} adverse authority/ies addressed.",
    )


def check_format_compliance(evidence: dict[str, Any]) -> CheckResult:
    """Check Bluebook/ALWD/local rules are followed."""
    citation_format = evidence.get("citation_format", "")
    format_errors = evidence.get("format_errors", [])

    if not citation_format:
        return CheckResult(
            check_id="format_compliance",
            name="Format Compliance",
            status="WARN",
            severity=Severity.MINOR,
            message="No citation format standard specified.",
            suggestions=["Set citation_format convention (Bluebook, ALWD, or local rules)."],
        )

    if format_errors:
        return CheckResult(
            check_id="format_compliance",
            name="Format Compliance",
            status="FAIL",
            severity=Severity.MINOR,
            message=f"{len(format_errors)} citation format error(s) found.",
            evidence={"errors": format_errors},
        )

    return CheckResult(
        check_id="format_compliance",
        name="Format Compliance",
        status="PASS",
        severity=Severity.MINOR,
        message=f"All citations comply with {citation_format} format.",
    )


def check_ethical_compliance(evidence: dict[str, Any]) -> CheckResult:
    """Check for Rule 11 (frivolousness) and Rule 3.3 (candor) compliance."""
    rule_11_concerns = evidence.get("rule_11_concerns", [])
    candor_issues = evidence.get("candor_issues", [])
    meritless_arguments = evidence.get("meritless_arguments", [])

    issues = rule_11_concerns + candor_issues + meritless_arguments

    if issues:
        return CheckResult(
            check_id="ethical_compliance",
            name="Ethical Compliance",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"Found {len(issues)} potential ethical compliance issue(s).",
            evidence={
                "rule_11": rule_11_concerns,
                "candor": candor_issues,
                "meritless": meritless_arguments,
            },
            suggestions=[
                "Review Fed. R. Civ. P. 11 for frivolousness standards.",
                "Review Model Rule 3.3 for candor obligations.",
                "Remove or reframe arguments that lack legal or factual basis.",
            ],
        )

    return CheckResult(
        check_id="ethical_compliance",
        name="Ethical Compliance",
        status="PASS",
        severity=Severity.CRITICAL,
        message="No ethical compliance concerns identified.",
    )


# -- Default predicate registry -----------------------------------------------

DEFAULT_PREDICATES: dict[str, Predicate] = {
    "citation_existence": check_citation_existence,
    "holding_accuracy": check_holding_accuracy,
    "subsequent_history": check_subsequent_history,
    "good_law_status": check_good_law_status,
    "standard_of_review": check_standard_of_review,
    "jurisdictional_accuracy": check_jurisdictional_accuracy,
    "statutory_currency": check_statutory_currency,
    "quotation_accuracy": check_quotation_accuracy,
    "logical_validity": check_logical_validity,
    "completeness": check_completeness,
    "format_compliance": check_format_compliance,
    "ethical_compliance": check_ethical_compliance,
}


# -- Verification Kernel ------------------------------------------------------

class VerificationKernel:
    """Content-addressed verification kernel for legal research.

    Runs predicates over evidence registries and produces
    SHA-256 verdicts for reproducibility and tamper-evidence.

    This kernel is THE critical defense against hallucinated citations,
    incorrect holdings, and other LLM legal errors.
    """

    def __init__(self, predicates: dict[str, Predicate] | None = None):
        self.predicates = predicates or dict(DEFAULT_PREDICATES)

    def _hash(self, data: str) -> str:
        return f"sha256:{hashlib.sha256(data.encode()).hexdigest()}"

    def verify(self, evidence: dict[str, Any]) -> Verdict:
        """Run all predicates against evidence and produce a verdict."""
        # Hash inputs
        evidence_json = json.dumps(evidence, sort_keys=True, default=str)
        registry_hash = self._hash(evidence_json)

        predicate_names = json.dumps(sorted(self.predicates.keys()))
        predicates_hash = self._hash(predicate_names)

        # Run predicates
        results: dict[str, CheckResult] = {}
        for check_id, predicate in self.predicates.items():
            try:
                result = predicate(evidence)
                results[check_id] = result
            except Exception as e:
                results[check_id] = CheckResult(
                    check_id=check_id,
                    name=check_id.replace("_", " ").title(),
                    status="FAIL",
                    severity=Severity.MAJOR,
                    message=f"Predicate raised exception: {e}",
                )

        # Determine overall status
        has_critical_fail = any(
            r.status == "FAIL" and r.severity == Severity.CRITICAL
            for r in results.values()
        )
        has_major_fail = any(
            r.status == "FAIL" and r.severity == Severity.MAJOR
            for r in results.values()
        )

        if has_critical_fail:
            overall = "FAIL"
        elif has_major_fail:
            overall = "PARTIAL"
        else:
            overall = "PASS"

        # Hash the results for tamper-evidence
        results_json = json.dumps(
            {k: v.message for k, v in results.items()},
            sort_keys=True,
        )
        verdict_hash = self._hash(
            f"{registry_hash}:{predicates_hash}:{results_json}"
        )

        # Build summary
        pass_count = sum(1 for r in results.values() if r.status == "PASS")
        fail_count = sum(1 for r in results.values() if r.status == "FAIL")
        skip_count = sum(1 for r in results.values() if r.status == "SKIP")
        warn_count = sum(1 for r in results.values() if r.status == "WARN")

        summary = (
            f"{overall}: {pass_count} passed, {fail_count} failed, "
            f"{warn_count} warnings, {skip_count} skipped "
            f"out of {len(results)} checks."
        )

        return Verdict(
            registry_hash=registry_hash,
            predicates_hash=predicates_hash,
            verdict_hash=verdict_hash,
            overall=overall,
            results=results,
            summary=summary,
        )
