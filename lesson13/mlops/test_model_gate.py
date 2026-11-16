
import pytest

from lesson13.mlops.model_gate import (
    ModelMetrics,
    evaluate_candidate,
)


CHAMPION = ModelMetrics(
    auc=0.9593,
    precision=0.9406,
    recall=0.7393,
)


def test_better_model_passes():
    candidate = ModelMetrics(
        auc=0.9700,
        precision=0.9500,
        recall=0.8000,
    )

    result = evaluate_candidate(candidate, CHAMPION)

    assert result.approved is True
    assert result.reasons == []


def test_auc_regression_fails():
    candidate = ModelMetrics(
        auc=0.9400,
        precision=0.9500,
        recall=0.8000,
    )

    result = evaluate_candidate(candidate, CHAMPION)

    assert result.approved is False
    assert any("AUC regression" in r for r in result.reasons)


def test_recall_regression_fails():
    candidate = ModelMetrics(
        auc=0.9700,
        precision=0.9500,
        recall=0.7000,
    )

    result = evaluate_candidate(candidate, CHAMPION)

    assert result.approved is False
    assert any("Recall regression" in r for r in result.reasons)


def test_small_regression_allowed():
    candidate = ModelMetrics(
        auc=0.9570,
        precision=0.9300,
        recall=0.7300,
    )

    result = evaluate_candidate(candidate, CHAMPION)

    assert result.approved is True


def test_absolute_auc_floor():
    champion = ModelMetrics(
        auc=0.8900,
        precision=0.8000,
        recall=0.7000,
    )

    candidate = ModelMetrics(
        auc=0.8950,
        precision=0.8500,
        recall=0.7500,
    )

    result = evaluate_candidate(candidate, champion)

    assert result.approved is False
    assert any("minimum" in r for r in result.reasons)


@pytest.mark.parametrize(
    "invalid_auc",
    [-0.1, 1.1],
)
def test_invalid_metric_rejected(invalid_auc):
    candidate = ModelMetrics(
        auc=invalid_auc,
        precision=0.95,
        recall=0.80,
    )

    result = evaluate_candidate(candidate, CHAMPION)

    assert result.approved is False
