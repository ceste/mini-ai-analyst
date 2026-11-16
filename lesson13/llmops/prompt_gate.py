from dataclasses import dataclass


@dataclass(frozen=True)
class PromptEvaluation:
    version: str
    pass_rate: float
    safety_pass_rate: float
    mean_latency_ms: float
    total_cases: int


@dataclass(frozen=True)
class GateDecision:
    approved: bool
    reasons: list[str]


def evaluate_prompt_release(
    candidate: PromptEvaluation,
    baseline: PromptEvaluation,
    min_pass_rate: float = 0.95,
    max_latency_multiplier: float = 3.0,
) -> GateDecision:

    reasons = []

    for name, evaluation in [
        ("candidate", candidate),
        ("baseline", baseline),
    ]:
        if not 0 <= evaluation.pass_rate <= 1:
            reasons.append(f"{name} pass rate is invalid")

        if not 0 <= evaluation.safety_pass_rate <= 1:
            reasons.append(f"{name} safety pass rate is invalid")

        if evaluation.mean_latency_ms <= 0:
            reasons.append(f"{name} latency is invalid")

        if evaluation.total_cases <= 0:
            reasons.append(f"{name} test count is invalid")

    if reasons:
        return GateDecision(False, reasons)

    if candidate.pass_rate < min_pass_rate:
        reasons.append(
            f"Pass rate {candidate.pass_rate:.1%} "
            f"is below minimum {min_pass_rate:.1%}"
        )

    if candidate.pass_rate < baseline.pass_rate:
        reasons.append("Candidate quality regressed")

    if candidate.safety_pass_rate < 1.0:
        reasons.append("Safety tests must pass 100%")

    if candidate.mean_latency_ms > (
        baseline.mean_latency_ms * max_latency_multiplier
    ):
        reasons.append("Latency exceeds allowed multiplier")

    return GateDecision(
        approved=len(reasons) == 0,
        reasons=reasons,
    )
