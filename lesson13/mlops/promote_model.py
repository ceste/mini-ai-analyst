import argparse
import math
import sys
from pathlib import Path

import mlflow
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException

from lesson13.mlops.model_gate import (
    ModelMetrics,
    evaluate_candidate,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "lesson13" / "mlops" / "mlflow.db"

MODEL_NAME = "customer-churn-classifier"
ALIAS = "champion"

mlflow.set_tracking_uri(f"sqlite:///{DB_PATH.as_posix()}")

client = MlflowClient()


def get_metrics(run_id: str) -> ModelMetrics:
    """Retrieve actual evaluation metrics from an MLflow run."""

    run = client.get_run(run_id)
    metrics = run.data.metrics

    required = ("auc", "precision", "recall")

    missing = [key for key in required if key not in metrics]

    if missing:
        raise ValueError(
            f"Run {run_id} is missing metrics: {missing}"
        )

    values = [float(metrics[key]) for key in required]

    if not all(math.isfinite(value) for value in values):
        raise ValueError("Non-finite metrics are not allowed")

    return ModelMetrics(
        auc=values[0],
        precision=values[1],
        recall=values[2],
    )


def promote(candidate_version: str, apply: bool = False) -> bool:

    # Get current champion
    champion = client.get_model_version_by_alias(
        MODEL_NAME,
        ALIAS,
    )

    # Get candidate version
    candidate = client.get_model_version(
        MODEL_NAME,
        candidate_version,
    )

    if not champion.run_id or not candidate.run_id:
        raise ValueError(
            "Both model versions must reference MLflow runs"
        )

    champion_metrics = get_metrics(champion.run_id)
    candidate_metrics = get_metrics(candidate.run_id)

    print(f"\nCurrent champion: version {champion.version}")
    print(f"Candidate: version {candidate.version}")

    print("\nChampion metrics:", champion_metrics)
    print("Candidate metrics:", candidate_metrics)

    # Compare using our previously tested policy
    result = evaluate_candidate(
        candidate=candidate_metrics,
        champion=champion_metrics,
    )

    print("\nValidation result:")
    print("APPROVED" if result.approved else "REJECTED")

    if not result.approved:
        for reason in result.reasons:
            print(" -", reason)
        return False

    if candidate.version == champion.version:
        print("Candidate is already champion.")
        return True

    if not apply:
        print("\nDRY RUN: No registry changes made.")
        print("Use --apply to promote the candidate.")
        return True

    # Recheck alias immediately before mutation.
    # This reduces, but does not eliminate, concurrency risk.
    latest = client.get_model_version_by_alias(
        MODEL_NAME,
        ALIAS,
    )

    if latest.version != champion.version:
        raise RuntimeError(
            "Champion changed during validation; aborting"
        )

    client.set_registered_model_alias(
        name=MODEL_NAME,
        alias=ALIAS,
        version=candidate.version,
    )

    print(f"\nPromoted version {candidate.version} to champion.")
    return True


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--candidate-version",
        required=True,
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually update the champion alias",
    )

    args = parser.parse_args()

    try:
        approved = promote(
            candidate_version=args.candidate_version,
            apply=args.apply,
        )
        return 0 if approved else 1

    except (MlflowException, ValueError, RuntimeError) as exc:
        print(f"Promotion error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
