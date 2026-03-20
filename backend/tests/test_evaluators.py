from evals.tool_usage import evaluate_tool_usage


def test_tool_usage_evaluator_marks_correct_primary_tool():
    result = evaluate_tool_usage("search_attractions", ["search_attractions", "search_web"])
    assert result.label == "correct"
    assert result.score == 1.0


def test_tool_usage_evaluator_marks_missing_tool_as_incorrect():
    result = evaluate_tool_usage("search_web", [])
    assert result.label == "incorrect"
    assert result.score == 0.0
