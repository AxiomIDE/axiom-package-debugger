from gen.axiom_official_axiom_agent_messages_messages_pb2 import AnalysisResult, AgentProgress


def handle(analysis: AnalysisResult, context) -> AgentProgress:
    """Route fix instructions to the package builder sub-flow or report success."""
    if not analysis.has_error:
        return AgentProgress(
            stage="complete",
            message="Package debug analysis complete — no code errors found.",
            complete=True,
            success=True,
        )

    return AgentProgress(
        stage="fix_required",
        message=f"Fix required: {analysis.error_summary}\n\n{analysis.fix_instructions}",
        complete=False,
        success=False,
    )
