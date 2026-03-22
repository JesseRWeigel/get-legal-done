"""Research contracts — Pydantic models for legal claims, deliverables, and acceptance tests.

Adapted from GPD's contracts.py for legal research and brief writing.

LEGAL DISCLAIMER: This is a research assistance tool, not a substitute for
licensed legal counsel. All output must be independently verified.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any


class LegalClaim(BaseModel):
    """A legal claim or argument to be researched and supported."""

    id: str
    statement: str
    claim_type: str = "argument"  # argument | counterargument | affirmative_defense | motion | objection
    legal_theory: str = ""  # negligence, breach_of_contract, due_process, etc.
    supporting_authorities: list[str] = Field(default_factory=list)  # Case/statute citations
    opposing_authorities: list[str] = Field(default_factory=list)
    depends_on: list[str] = Field(default_factory=list)  # Other claim IDs
    status: str = "unresearched"  # unresearched | researched | supported | unsupported | partial
    jurisdiction: str = ""
    standard_of_review: str = ""


class Deliverable(BaseModel):
    """An expected output artifact from a phase/plan."""

    id: str
    description: str
    artifact_type: str  # brief | memorandum | motion | research_memo | case_summary | statutory_analysis | citation_report
    file_path: str = ""
    acceptance_tests: list[str] = Field(default_factory=list)
    status: str = "pending"  # pending | delivered | verified | rejected


class AcceptanceTest(BaseModel):
    """A concrete test for a deliverable."""

    id: str
    description: str
    test_type: str  # citation_exists | holding_accurate | good_law | format_compliant | completeness | logical_validity
    predicate: str = ""  # Human-readable predicate
    status: str = "pending"  # pending | passed | failed


class ForbiddenProxy(BaseModel):
    """Something that must NOT be used as evidence of completion.

    Prevents agents from claiming success based on superficial signals.
    """

    description: str
    reason: str


class ResearchContract(BaseModel):
    """A complete research contract for a phase or plan.

    Defines what must be achieved, how to verify it, and what NOT to accept.
    """

    phase_id: str
    plan_id: str = ""
    goal: str

    claims: list[LegalClaim] = Field(default_factory=list)
    deliverables: list[Deliverable] = Field(default_factory=list)
    acceptance_tests: list[AcceptanceTest] = Field(default_factory=list)

    forbidden_proxies: list[ForbiddenProxy] = Field(
        default_factory=lambda: [
            ForbiddenProxy(
                description="Agent citing a case without verifying it exists",
                reason="Every citation must be verified against a real database (CourtListener, Westlaw, etc.).",
            ),
            ForbiddenProxy(
                description="Stating a holding without quoting or paraphrasing the actual opinion",
                reason="Holdings must be traceable to specific language in the opinion.",
            ),
            ForbiddenProxy(
                description="Claiming research is complete without checking adverse authority",
                reason="Ethical obligation requires addressing contrary authority (Model Rule 3.3).",
            ),
            ForbiddenProxy(
                description="Using a citation format without verifying local rules",
                reason="Courts have specific citation format requirements that vary by jurisdiction.",
            ),
            ForbiddenProxy(
                description="Presenting AI-generated legal analysis as attorney work product",
                reason="All output must be reviewed and verified by licensed counsel.",
            ),
        ]
    )

    def all_claims_resolved(self) -> bool:
        return all(c.status in ("supported", "unsupported") for c in self.claims)

    def all_deliverables_verified(self) -> bool:
        return all(d.status == "verified" for d in self.deliverables)

    def all_tests_passed(self) -> bool:
        return all(t.status == "passed" for t in self.acceptance_tests)


class AgentReturn(BaseModel):
    """Structured return envelope from subagents.

    Every subagent MUST produce this in their SUMMARY.md.
    The orchestrator uses this — not prose — to determine success.
    """

    status: str  # completed | checkpoint | blocked | failed
    files_written: list[str] = Field(default_factory=list)
    files_modified: list[str] = Field(default_factory=list)
    issues: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
    claims_supported: list[str] = Field(default_factory=list)  # Claim IDs
    citations_verified: list[str] = Field(default_factory=list)  # Verified citation strings
    citations_flagged: list[str] = Field(default_factory=list)  # Citations needing review
    conventions_proposed: dict[str, str] = Field(default_factory=dict)
    verification_evidence: dict[str, Any] = Field(default_factory=dict)
