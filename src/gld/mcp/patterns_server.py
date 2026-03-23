"""MCP server for GLD legal research patterns and best practices.

Exposes tools for querying legal research phases, research mode management,
autonomy settings, and legal methodology patterns.
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from gld.core.state import StateEngine
from gld.core.constants import (
    ProjectLayout,
    VALID_AUTONOMY_MODES,
    VALID_RESEARCH_MODES,
    VERIFICATION_CHECKS,
    CONVENTION_FIELDS,
    SEVERITY_CRITICAL,
    SEVERITY_MAJOR,
    SEVERITY_MINOR,
    SEVERITY_NOTE,
)

server = Server("gld-patterns")


def _get_engine(project_root: str | None = None) -> StateEngine:
    if project_root:
        return StateEngine(layout=ProjectLayout(root=Path(project_root)))
    return StateEngine()


# -- Legal research phase patterns --

LEGAL_PHASES = [
    {"id": "1", "title": "Issue Identification", "description": "Analyze fact pattern, identify all legal issues and potential claims."},
    {"id": "2", "title": "Jurisdiction & Posture", "description": "Determine jurisdiction, procedural posture, and applicable standards."},
    {"id": "3", "title": "Case Law Research", "description": "Find binding and persuasive authority, Shepardize/KeyCite all cases."},
    {"id": "4", "title": "Statutory Research", "description": "Research applicable statutes, regulations, and legislative history."},
    {"id": "5", "title": "Legal Analysis", "description": "Construct arguments using IRAC/CREAC, address adverse authority."},
    {"id": "6", "title": "Drafting", "description": "Draft brief/memorandum/motion with proper citation format."},
]


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_legal_phases",
            description="Get the standard legal research phase sequence with descriptions.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="get_severity_levels",
            description="Get verification severity levels and their meanings.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="set_research_mode",
            description="Set the research mode (explore, balanced, exploit, adaptive).",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                    "mode": {
                        "type": "string",
                        "enum": list(VALID_RESEARCH_MODES),
                        "description": "Research mode to set.",
                    },
                },
                "required": ["mode"],
            },
        ),
        Tool(
            name="set_autonomy_mode",
            description="Set the autonomy mode (supervised, balanced, yolo).",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                    "mode": {
                        "type": "string",
                        "enum": list(VALID_AUTONOMY_MODES),
                        "description": "Autonomy mode to set.",
                    },
                },
                "required": ["mode"],
            },
        ),
        Tool(
            name="get_project_summary",
            description="Get a high-level summary of the project including phase progress, convention coverage, and verification stats.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "get_legal_phases":
        return [TextContent(type="text", text=json.dumps(LEGAL_PHASES, indent=2))]

    elif name == "get_severity_levels":
        levels = [
            {"level": SEVERITY_CRITICAL, "description": "Blocks all downstream work."},
            {"level": SEVERITY_MAJOR, "description": "Must resolve before drawing conclusions."},
            {"level": SEVERITY_MINOR, "description": "Must resolve before filing."},
            {"level": SEVERITY_NOTE, "description": "Informational only."},
        ]
        return [TextContent(type="text", text=json.dumps(levels, indent=2))]

    engine = _get_engine(arguments.get("project_root"))

    if name == "set_research_mode":
        mode = arguments["mode"]
        if mode not in VALID_RESEARCH_MODES:
            return [TextContent(type="text", text=json.dumps({"error": f"Invalid mode: {mode}", "valid": list(VALID_RESEARCH_MODES)}))]
        state = engine.load()
        state.research_mode = mode
        engine.save(state)
        return [TextContent(type="text", text=json.dumps({"status": "set", "research_mode": mode}))]

    elif name == "set_autonomy_mode":
        mode = arguments["mode"]
        if mode not in VALID_AUTONOMY_MODES:
            return [TextContent(type="text", text=json.dumps({"error": f"Invalid mode: {mode}", "valid": list(VALID_AUTONOMY_MODES)}))]
        state = engine.load()
        state.autonomy_mode = mode
        engine.save(state)
        return [TextContent(type="text", text=json.dumps({"status": "set", "autonomy_mode": mode}))]

    elif name == "get_project_summary":
        state = engine.load()
        phases_complete = sum(1 for p in state.phases.values() if p.status == "completed")
        phases_total = len(state.phases)
        conventions_locked = len(state.conventions)
        conventions_total = len(CONVENTION_FIELDS)
        total_verifications = state.total_verification_passes + state.total_verification_failures
        return [TextContent(type="text", text=json.dumps({
            "project_name": state.project_name,
            "current_milestone": state.current_milestone,
            "current_phase": state.current_phase,
            "research_mode": state.research_mode,
            "autonomy_mode": state.autonomy_mode,
            "phases_progress": f"{phases_complete}/{phases_total}",
            "conventions_coverage": f"{conventions_locked}/{conventions_total}",
            "tasks_completed": state.total_tasks_completed,
            "verification_pass_rate": round(
                state.total_verification_passes / max(1, total_verifications) * 100, 1
            ),
            "decisions_count": len(state.decisions),
        }, indent=2))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
