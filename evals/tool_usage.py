from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence


@dataclass(frozen=True)
class ToolUsageEvaluation:
    label: str
    score: float
    explanation: str

    def to_annotation_result(self) -> dict[str, object]:
        return asdict(self)


def evaluate_tool_usage(
    expected_primary_tool: str,
    observed_tool_names: Sequence[str],
) -> ToolUsageEvaluation:
    observed = [tool for tool in observed_tool_names if tool]
    if expected_primary_tool == "none":
        if observed:
            return ToolUsageEvaluation(
                label="incorrect",
                score=0.0,
                explanation=f"Expected the agent to answer without tools, but it used {', '.join(observed)}.",
            )
        return ToolUsageEvaluation(
            label="correct",
            score=1.0,
            explanation="The agent answered without invoking any tools, as expected.",
        )

    if not observed:
        return ToolUsageEvaluation(
            label="incorrect",
            score=0.0,
            explanation=f"Expected `{expected_primary_tool}` but no tool calls were observed.",
        )

    primary_observed = observed[0]
    if primary_observed == expected_primary_tool:
        return ToolUsageEvaluation(
            label="correct",
            score=1.0,
            explanation=f"The first observed tool `{primary_observed}` matched the expected primary tool.",
        )
    return ToolUsageEvaluation(
        label="incorrect",
        score=0.0,
        explanation=(
            f"Expected `{expected_primary_tool}` as the primary tool, "
            f"but observed `{primary_observed}` first."
        ),
    )
