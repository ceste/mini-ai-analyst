from dataclasses import dataclass


@dataclass(frozen=True)
class ModelMetrics:
    auc: float
    precision: float
    recall: float


@dataclass(frozen=True)
class GateResult:
    approved: bool
    reasons: list[str]


def evaluate_candidate(
    candidate: ModelMetrics,
    champion: ModelMetrics,
    min_auc: float = 0.90,
    max_auc_regression: float = 0.005,
    max_recall_regression: float = 0.02,
) -> GateResult:
    """
    Evaluate whether a candidate meets promotion requirements.

    All metrics are proportions between 0 and 1.
    """
    reasons = []

    for name, metrics in [
        ("candidate", candidate),
        ("champion", champion),
    ]:
        for metric_name in ("auc", "precision", "recall"):
            value = getattr(metrics, metric_name)

            if not 0 <= value <= 1:
                reasons.append(
                    f"{name}.{metric_name} must be between 0 and 1"
                )

    if reasons:
        return GateResult(False, reasons)

    if candidate.auc < min_auc:
        reasons.append(
            f"AUC {candidate.auc:.4f} is below "
            f"minimum {min_auc:.4f}"
        )

    if candidate.auc < champion.auc - max_auc_regression:
        reasons.append(
            f"AUC regression exceeds {max_auc_regression:.4f}"
        )

    if candidate.recall < champion.recall - max_recall_regression:
        reasons.append(
            f"Recall regression exceeds "
            f"{max_recall_regression:.4f}"
        )

    return GateResult(
        approved=len(reasons) == 0,
        reasons=reasons,
    )
