"""Convention lock management for legal research consistency.

Ensures jurisdictional choices, citation formats, and legal frameworks
don't drift across phases of a legal research project.
Adapted from GPD's conventions.py for legal research.
"""

from __future__ import annotations

from typing import Any

from .constants import CONVENTION_FIELDS
from .state import StateEngine, ConventionLock


# -- Convention Field Descriptions --------------------------------------------

CONVENTION_DESCRIPTIONS: dict[str, str] = {
    "jurisdiction": (
        "The court and jurisdiction for this matter: federal vs state, "
        "specific circuit (1st-11th, D.C., Federal), district court, "
        "state court system and level. Determines what authority is binding."
    ),
    "governing_law": (
        "Which body of law governs the substantive issues: state law "
        "(specify which state), federal law, or a combination. For diversity "
        "cases, Erie doctrine determines which state's law applies."
    ),
    "standard_of_review": (
        "The standard the court applies when reviewing the issue: "
        "de novo (questions of law), abuse of discretion (procedural rulings), "
        "clearly erroneous (findings of fact after bench trial), "
        "substantial evidence (administrative review), rational basis / "
        "intermediate / strict scrutiny (constitutional questions)."
    ),
    "burden_of_proof": (
        "Who bears the burden and what standard: preponderance of the "
        "evidence (most civil), clear and convincing evidence (fraud, "
        "punitive damages, some family law), beyond a reasonable doubt "
        "(criminal). Also note any burden-shifting frameworks (McDonnell Douglas, etc.)."
    ),
    "citation_format": (
        "Citation style to follow: Bluebook (20th/21st ed.), ALWD Guide "
        "to Legal Citation, or specific local court rules. Many courts have "
        "their own citation format requirements that override Bluebook."
    ),
    "procedural_posture": (
        "Current stage of the case: motion to dismiss (12(b)(6)), "
        "summary judgment, trial, post-trial motions, appeal, habeas "
        "corpus, interlocutory appeal, certiorari. Determines applicable "
        "standards and available arguments."
    ),
    "cause_of_action": (
        "The specific legal theory or claim: negligence, breach of contract, "
        "42 U.S.C. 1983, Title VII discrimination, patent infringement, "
        "RICO, antitrust (Sherman Act), securities fraud (10b-5), etc. "
        "Lock this to prevent scope drift."
    ),
    "statute_of_limitations": (
        "The applicable limitations period and any tolling doctrines: "
        "discovery rule, equitable tolling, fraudulent concealment, "
        "relation back doctrine. Note the specific statute and period."
    ),
    "damages_theory": (
        "The theory of damages being pursued: compensatory (economic + "
        "non-economic), punitive/exemplary, statutory damages, liquidated "
        "damages, equitable relief (injunction, specific performance, "
        "restitution), nominal damages, treble damages."
    ),
    "key_definitions": (
        "Jurisdiction-specific terms of art that have particular legal "
        "meaning in this context. Examples: 'employee' vs 'independent "
        "contractor' under the applicable test, 'willful' under the "
        "relevant statute, 'material' in the specific legal context."
    ),
}

# -- Convention Validation ----------------------------------------------------

# Common valid values for quick validation
CONVENTION_EXAMPLES: dict[str, list[str]] = {
    "jurisdiction": [
        "U.S. District Court, Southern District of New York",
        "U.S. Court of Appeals, Ninth Circuit",
        "California Superior Court, Los Angeles County",
        "U.S. Supreme Court",
    ],
    "standard_of_review": [
        "De novo",
        "Abuse of discretion",
        "Clearly erroneous",
        "Substantial evidence",
        "Rational basis",
        "Intermediate scrutiny",
        "Strict scrutiny",
    ],
    "burden_of_proof": [
        "Preponderance of the evidence (plaintiff)",
        "Clear and convincing evidence (plaintiff)",
        "Beyond a reasonable doubt (prosecution)",
        "McDonnell Douglas burden-shifting framework",
    ],
    "citation_format": [
        "Bluebook (21st ed.)",
        "ALWD Guide to Legal Citation (7th ed.)",
        "California Style Manual",
        "Local Rule 7.1 (S.D.N.Y.)",
    ],
    "procedural_posture": [
        "Motion to dismiss under Fed. R. Civ. P. 12(b)(6)",
        "Motion for summary judgment under Fed. R. Civ. P. 56",
        "Appeal from final judgment",
        "Petition for writ of certiorari",
    ],
}


def get_field_description(field: str) -> str:
    """Get the description for a convention field."""
    return CONVENTION_DESCRIPTIONS.get(field, f"Convention field: {field}")


def get_field_examples(field: str) -> list[str]:
    """Get example values for a convention field."""
    return CONVENTION_EXAMPLES.get(field, [])


def list_all_fields() -> list[dict[str, Any]]:
    """List all convention fields with descriptions and examples."""
    return [
        {
            "field": f,
            "description": get_field_description(f),
            "examples": get_field_examples(f),
        }
        for f in CONVENTION_FIELDS
    ]


def check_conventions(engine: StateEngine) -> dict[str, Any]:
    """Check which conventions are locked and which are missing.

    Returns a report dict with locked, unlocked, and coverage stats.
    """
    state = engine.load()
    locked = {}
    unlocked = []

    for field in CONVENTION_FIELDS:
        if field in state.conventions:
            locked[field] = {
                "value": state.conventions[field].value,
                "locked_by": state.conventions[field].locked_by,
                "rationale": state.conventions[field].rationale,
            }
        else:
            unlocked.append(field)

    return {
        "locked": locked,
        "unlocked": unlocked,
        "coverage": f"{len(locked)}/{len(CONVENTION_FIELDS)}",
        "coverage_pct": round(100 * len(locked) / len(CONVENTION_FIELDS), 1)
        if CONVENTION_FIELDS
        else 100.0,
    }


def diff_conventions(
    engine: StateEngine,
    proposed: dict[str, str],
) -> dict[str, Any]:
    """Compare proposed convention values against current locks.

    Returns conflicts, new fields, and matching fields.
    """
    state = engine.load()
    conflicts = {}
    new_fields = {}
    matching = {}

    for field, proposed_value in proposed.items():
        if field in state.conventions:
            current = state.conventions[field].value
            if current != proposed_value:
                conflicts[field] = {
                    "current": current,
                    "proposed": proposed_value,
                }
            else:
                matching[field] = current
        else:
            new_fields[field] = proposed_value

    return {
        "conflicts": conflicts,
        "new_fields": new_fields,
        "matching": matching,
        "has_conflicts": bool(conflicts),
    }
