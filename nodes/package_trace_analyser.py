import json
import os

import anthropic

from gen.axiom_official_axiom_agent_messages_messages_pb2 import PackageBuildContext
from gen.axiom_logger import AxiomLogger, AxiomSecrets


SYSTEM_PROMPT = """You are an expert at diagnosing Axiom node failures from debug traces.
Identify the root cause and produce actionable fix instructions."""


def package_trace_analyser(log: AxiomLogger, secrets: AxiomSecrets, input: PackageBuildContext) -> PackageBuildContext:
    if input.test_success:
        input.has_error = False
        input.error_summary = "No errors found"
        return input

    api_key = secrets.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY", "")
    client = anthropic.Anthropic(api_key=api_key)

    debug_events = ""
    if input.fix_instructions:
        try:
            data = json.loads(input.fix_instructions)
            debug_events = json.dumps(data.get("debug_events", data), indent=2)[:4000]
        except Exception:
            debug_events = input.fix_instructions[:4000]

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"""Analyse this package test failure:

Error: {input.test_error}

Debug trace:
{debug_events or "(none)"}

Identify root cause and provide fix instructions."""
        }]
    )

    input.has_error = True
    input.fix_instructions = message.content[0].text
    input.error_summary = (input.test_error or "Unknown error")[:200]
    input.iteration = input.iteration + 1

    return input
