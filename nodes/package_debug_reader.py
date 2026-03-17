import json
import os

import httpx

from gen.axiom_official_axiom_agent_messages_messages_pb2 import PackageBuildContext
from gen.axiom_logger import AxiomLogger, AxiomSecrets


def package_debug_reader(log: AxiomLogger, secrets: AxiomSecrets, input: PackageBuildContext) -> PackageBuildContext:
    """Fetch the debug event stream and attach it to the context for analysis."""

    if not input.session_id:
        return input

    ingress_url = os.environ.get("INGRESS_URL", "http://axiom-ingress:80")
    axiom_api_key, _ = secrets.get("AXIOM_API_KEY")
    tenant_id = os.environ.get("TENANT_ID", "01AXIOMOFFICIAL000000000000")

    try:
        resp = httpx.get(
            f"{ingress_url}/v1/debug-events",
            params={"session_id": input.session_id, "limit": "100"},
            headers={
                "Authorization": f"Bearer {axiom_api_key}",
                "X-Tenant-Id": tenant_id,
            },
            timeout=10.0,
        )
        if resp.status_code == 200:
            events = resp.json()
            # Attach the raw debug events as JSON in fix_instructions for downstream analysis.
            input.fix_instructions = json.dumps({"debug_events": events})
    except Exception as e:
        log.warn(f"Failed to fetch debug events: {e}")

    return input
