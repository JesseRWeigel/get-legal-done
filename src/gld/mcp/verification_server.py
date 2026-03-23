"""MCP server for GLD verification kernel.

Exposes tools for running the 12 legal verification predicates
over evidence registries and producing SHA-256 verdicts.
Critical defense against hallucinated citations and incorrect holdings.
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

from gld.core.kernel import VerificationKernel, DEFAULT_PREDICATES, VERIFICATION_CHECKS

server = Server("gld-verification")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="verify",
            description=(
                "Run all 12 legal verification checks against an evidence registry. "
                "Returns a content-addressed verdict with SHA-256 hashes. "
                "Checks: citation existence, holding accuracy, subsequent history, "
                "good law status, standard of review, jurisdictional accuracy, "
                "statutory currency, quotation accuracy, logical validity, "
                "completeness (adverse authority), format compliance, ethical compliance."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "evidence": {
                        "type": "object",
                        "description": (
                            "Evidence registry dict. Keys include: citations, verified_citations, "
                            "unverified_citations, hallucinated_citations, holdings_claimed, "
                            "holdings_verified, holdings_inaccurate, cases_shepardized, "
                            "negative_history, authorities_checked, bad_law, superseded_statutes, "
                            "claimed_standard, correct_standard, procedural_posture, "
                            "authority_classifications, misclassified_authority, statutes_cited, "
                            "outdated_statutes, quotes, inaccurate_quotes, reasoning_steps, "
                            "logical_gaps, irac_complete, adverse_authority_identified, "
                            "adverse_authority_addressed, citation_format, format_errors, "
                            "rule_11_concerns, candor_issues, meritless_arguments."
                        ),
                    },
                },
                "required": ["evidence"],
            },
        ),
        Tool(
            name="list_checks",
            description="List all available legal verification checks with their IDs.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="run_single_check",
            description="Run a single named verification check against evidence.",
            inputSchema={
                "type": "object",
                "properties": {
                    "check_id": {
                        "type": "string",
                        "description": f"Check to run. Valid: {', '.join(VERIFICATION_CHECKS)}",
                    },
                    "evidence": {"type": "object"},
                },
                "required": ["check_id", "evidence"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "verify":
        kernel = VerificationKernel()
        verdict = kernel.verify(arguments["evidence"])
        return [TextContent(type="text", text=verdict.to_json())]

    elif name == "list_checks":
        from gld.core.constants import VERIFICATION_CHECKS as checks
        return [TextContent(type="text", text=json.dumps(checks, indent=2))]

    elif name == "run_single_check":
        check_id = arguments["check_id"]
        if check_id not in DEFAULT_PREDICATES:
            return [TextContent(type="text", text=json.dumps({
                "error": f"Unknown check: {check_id}",
                "available": list(DEFAULT_PREDICATES.keys()),
            }))]
        predicate = DEFAULT_PREDICATES[check_id]
        result = predicate(arguments["evidence"])
        return [TextContent(type="text", text=json.dumps({
            "check_id": result.check_id,
            "name": result.name,
            "status": result.status,
            "severity": result.severity.value,
            "message": result.message,
            "evidence": result.evidence,
            "suggestions": result.suggestions,
        }, indent=2))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
