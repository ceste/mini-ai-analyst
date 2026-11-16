from lesson13.llmops.prompt_gate import (
    PromptEvaluation,
    evaluate_prompt_release,
)


BASELINE = PromptEvaluation(
    version="v1",
    pass_rate=0.80,
    safety_pass_rate=1.0,
    mean_latency_ms=2502.63,
    total_cases=5,
)


def test_improved_prompt_passes():
    candidate = PromptEvaluation(
        version="v2",
        pass_rate=1.0,
        safety_pass_rate=1.0,
        mean_latency_ms=4338.30,
        total_cases=5,
    )

    result = evaluate_prompt_release(candidate, BASELINE)

    assert result.approved is True


def test_quality_regression_fails():
    candidate = PromptEvaluation(
        version="v3",
        pass_rate=0.60,
        safety_pass_rate=1.0,
        mean_latency_ms=2000,
        total_cases=5,
    )

    result = evaluate_prompt_release(candidate, BASELINE)

    assert result.approved is False


def test_safety_failure_blocks_release():
    candidate = PromptEvaluation(
        version="v3",
        pass_rate=1.0,
        safety_pass_rate=0.80,
        mean_latency_ms=2000,
        total_cases=5,
    )

    result = evaluate_prompt_release(candidate, BASELINE)

    assert result.approved is False
    assert any("Safety" in r for r in result.reasons)


def test_excessive_latency_blocks_release():
    candidate = PromptEvaluation(
        version="v3",
        pass_rate=1.0,
        safety_pass_rate=1.0,
        mean_latency_ms=9000,
        total_cases=5,
    )

    result = evaluate_prompt_release(candidate, BASELINE)

    assert result.approved is False
    assert any("Latency" in r for r in result.reasons)


def test_invalid_metrics_rejected():
    candidate = PromptEvaluation(
        version="v3",
        pass_rate=1.2,
        safety_pass_rate=1.0,
        mean_latency_ms=2000,
        total_cases=5,
    )

    result = evaluate_prompt_release(candidate, BASELINE)

    assert result.approved is False
