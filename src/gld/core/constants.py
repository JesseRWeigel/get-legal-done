"""Single source of truth for all directory/file names and environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


# -- Environment Variables ----------------------------------------------------

ENV_GLD_HOME = "GLD_HOME"
ENV_GLD_PROJECT = "GLD_PROJECT"
ENV_GLD_INSTALL_DIR = "GLD_INSTALL_DIR"
ENV_GLD_DEBUG = "GLD_DEBUG"
ENV_GLD_AUTONOMY = "GLD_AUTONOMY"

# -- File Names ---------------------------------------------------------------

STATE_MD = "STATE.md"
STATE_JSON = "state.json"
STATE_WRITE_INTENT = ".state-write-intent"
ROADMAP_MD = "ROADMAP.md"
CONFIG_JSON = "config.json"
CONVENTIONS_JSON = "conventions.json"

PLAN_PREFIX = "PLAN"
SUMMARY_PREFIX = "SUMMARY"
RESEARCH_MD = "RESEARCH.md"
RESEARCH_DIGEST_MD = "RESEARCH-DIGEST.md"
CONTINUE_HERE_MD = ".continue-here.md"

# -- Directory Names ----------------------------------------------------------

GLD_DIR = ".gld"
OBSERVABILITY_DIR = "observability"
SESSIONS_DIR = "sessions"
TRACES_DIR = "traces"
KNOWLEDGE_DIR = "knowledge"
BRIEFS_DIR = "briefs"
SCRATCH_DIR = ".scratch"

# -- Git ----------------------------------------------------------------------

CHECKPOINT_TAG_PREFIX = "gld-checkpoint"
COMMIT_PREFIX = "[gld]"

# -- Autonomy Modes -----------------------------------------------------------

AUTONOMY_SUPERVISED = "supervised"
AUTONOMY_BALANCED = "balanced"
AUTONOMY_YOLO = "yolo"
VALID_AUTONOMY_MODES = {AUTONOMY_SUPERVISED, AUTONOMY_BALANCED, AUTONOMY_YOLO}

# -- Research Modes ------------------------------------------------------------

RESEARCH_EXPLORE = "explore"
RESEARCH_BALANCED = "balanced"
RESEARCH_EXPLOIT = "exploit"
RESEARCH_ADAPTIVE = "adaptive"
VALID_RESEARCH_MODES = {RESEARCH_EXPLORE, RESEARCH_BALANCED, RESEARCH_EXPLOIT, RESEARCH_ADAPTIVE}

# -- Model Tiers --------------------------------------------------------------

TIER_1 = "tier-1"  # Highest capability
TIER_2 = "tier-2"  # Balanced
TIER_3 = "tier-3"  # Fastest

# -- Verification Severity ----------------------------------------------------

SEVERITY_CRITICAL = "CRITICAL"  # Blocks all downstream work
SEVERITY_MAJOR = "MAJOR"        # Must resolve before conclusions
SEVERITY_MINOR = "MINOR"        # Must resolve before filing
SEVERITY_NOTE = "NOTE"          # Informational

# -- Convention Lock Fields (Legal Research) -----------------------------------

CONVENTION_FIELDS = [
    "jurisdiction",               # Federal/state, circuit, district, court
    "governing_law",              # Which state/federal law governs
    "standard_of_review",         # De novo, abuse of discretion, clearly erroneous, rational basis, strict scrutiny
    "burden_of_proof",            # Preponderance, clear and convincing, beyond reasonable doubt
    "citation_format",            # Bluebook, ALWD, local court rules
    "procedural_posture",         # Trial, appeal, habeas, interlocutory, etc.
    "cause_of_action",            # Negligence, breach of contract, 42 USC 1983, etc.
    "statute_of_limitations",     # Applicable limitations framework
    "damages_theory",             # Compensatory, punitive, equitable, nominal
    "key_definitions",            # Jurisdiction-specific terms of art
]

# -- Verification Checks (Legal) ----------------------------------------------

VERIFICATION_CHECKS = [
    "citation_existence",         # Every cited case/statute/regulation actually exists
    "holding_accuracy",           # Holdings match actual judicial opinions
    "subsequent_history",         # Not reversed, vacated, or overruled
    "good_law_status",            # Still valid and citable
    "standard_of_review",         # Correct standard applied for the procedural posture
    "jurisdictional_accuracy",    # Binding vs persuasive authority correctly identified
    "statutory_currency",         # Citing current version of statutes, not superseded
    "quotation_accuracy",         # Direct quotes match source material exactly
    "logical_validity",           # Legal reasoning is sound (IRAC/CREAC structure)
    "completeness",               # Adverse authority addressed (Model Rule 3.3 compliance)
    "format_compliance",          # Bluebook/ALWD/local rules followed
    "ethical_compliance",         # Not frivolous (Rule 11), candor to tribunal (Rule 3.3)
]


@dataclass(frozen=True)
class ProjectLayout:
    """Resolved paths for a GLD project."""

    root: Path

    @property
    def gld_dir(self) -> Path:
        return self.root / GLD_DIR

    @property
    def state_md(self) -> Path:
        return self.gld_dir / STATE_MD

    @property
    def state_json(self) -> Path:
        return self.gld_dir / STATE_JSON

    @property
    def state_write_intent(self) -> Path:
        return self.gld_dir / STATE_WRITE_INTENT

    @property
    def roadmap_md(self) -> Path:
        return self.gld_dir / ROADMAP_MD

    @property
    def config_json(self) -> Path:
        return self.gld_dir / CONFIG_JSON

    @property
    def conventions_json(self) -> Path:
        return self.gld_dir / CONVENTIONS_JSON

    @property
    def observability_dir(self) -> Path:
        return self.gld_dir / OBSERVABILITY_DIR

    @property
    def sessions_dir(self) -> Path:
        return self.observability_dir / SESSIONS_DIR

    @property
    def traces_dir(self) -> Path:
        return self.gld_dir / TRACES_DIR

    @property
    def knowledge_dir(self) -> Path:
        return self.root / KNOWLEDGE_DIR

    @property
    def briefs_dir(self) -> Path:
        return self.root / BRIEFS_DIR

    @property
    def scratch_dir(self) -> Path:
        return self.root / SCRATCH_DIR

    @property
    def continue_here(self) -> Path:
        return self.gld_dir / CONTINUE_HERE_MD

    def phase_dir(self, phase: str) -> Path:
        return self.root / f"phase-{phase}"

    def plan_path(self, phase: str, plan_number: str) -> Path:
        return self.phase_dir(phase) / f"{PLAN_PREFIX}-{plan_number}.md"

    def summary_path(self, phase: str, plan_number: str) -> Path:
        return self.phase_dir(phase) / f"{SUMMARY_PREFIX}-{plan_number}.md"

    def ensure_dirs(self) -> None:
        """Create all required directories."""
        for d in [
            self.gld_dir,
            self.observability_dir,
            self.sessions_dir,
            self.traces_dir,
            self.knowledge_dir,
            self.scratch_dir,
        ]:
            d.mkdir(parents=True, exist_ok=True)


def find_project_root(start: Path | None = None) -> Path:
    """Walk up from start (or cwd) looking for .gld/ directory."""
    current = start or Path.cwd()
    while current != current.parent:
        if (current / GLD_DIR).is_dir():
            return current
        current = current.parent
    raise FileNotFoundError(
        f"No {GLD_DIR}/ directory found. Run 'gld init' to create a project."
    )


def get_layout(start: Path | None = None) -> ProjectLayout:
    """Get the project layout, finding the root automatically."""
    env_project = os.environ.get(ENV_GLD_PROJECT)
    if env_project:
        return ProjectLayout(root=Path(env_project))
    return ProjectLayout(root=find_project_root(start))
