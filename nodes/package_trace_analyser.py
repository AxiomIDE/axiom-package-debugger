import json
import os

import anthropic

from gen.axiom_official_axiom_agent_messages_messages_pb2 import TestResult, AnalysisResult
from gen.axiom_logger import AxiomLogger, AxiomSecrets


SYSTEM_PROMPT = """You are an expert at diagnosing Axiom node failures from debug traces.
Identify the root cause and produce actionable fix instructions."""


def package_trace_analyser(log: AxiomLogger, secrets: AxiomSecrets, input: TestResult) -> AnalysisResult:
    if input.success:
        return AnalysisResult(has_error=False, error_summary="No errors found")

    api_key = secrets.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY", "")
    client = anthropic.Anthropic(api_key=api_key)

    debug_events = ""
    if input.output_json:
        try:
            data = json.loads(input.output_json)
            debug_events = json.dumps(data.get("debug_events", data), indent=2)[:4000]
        except Exception:
            debug_events = input.output_json[:4000]

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"""Analyse this package test failure:

Error: {input.error}

Debug trace:
{debug_events or "(none)"}

Identify root cause and provide fix instructions."""
        }]
    )

    return AnalysisResult(
        has_error=True,
        fix_instructions=message.content[0].text,
        error_summary=input.error[:200] if input.error else "Unknown error",
        iteration=1,
    )
