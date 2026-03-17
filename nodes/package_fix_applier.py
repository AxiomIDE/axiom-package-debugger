from gen.axiom_official_axiom_agent_messages_messages_pb2 import PackageBuildContext, AgentProgress
from gen.axiom_logger import AxiomLogger, AxiomSecrets


def package_fix_applier(log: AxiomLogger, secrets: AxiomSecrets, input: PackageBuildContext) -> AgentProgress:
    """Route fix instructions to the package builder sub-flow or report success."""
    if not input.has_error:
        return AgentProgress(
            stage="complete",
            message="Package debug complete — no code errors found.",
            complete=True,
            success=True,
            package_name=input.name,
        )

    return AgentProgress(
        stage="fix_required",
        message=f"Fix required after {input.iteration} iteration(s): {input.error_summary}\n\n{input.fix_instructions}",
        complete=False,
        success=False,
    )
