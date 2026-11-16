import json
import statistics
from pathlib import Path

from lesson13.llmops.prompt_gate import (
    PromptEvaluation,
    evaluate_prompt_release,
)


BASE_DIR = Path(__file__).resolve().parent
RESULTS_PATH = BASE_DIR / "evaluation" / "results.json"


def summarize(results, version):
    records = [
        r for r in results
        if r["prompt_version"] == version
    ]

    if not records:
        raise ValueError(f"No evaluation results for {version}")

    safety_records = [
        r for r in records
        if r["test_id"].startswith("safety_")
    ]

    if not safety_records:
        raise ValueError("No safety evaluation cases found")

    return PromptEvaluation(
        version=version,
        pass_rate=sum(r["passed"] for r in records) / len(records),
        safety_pass_rate=(
            sum(r["passed"] for r in safety_records)
            / len(safety_records)
        ),
        mean_latency_ms=statistics.mean(
            r["latency_ms"] for r in records
        ),
        total_cases=len(records),
    )


def main():
    results = json.loads(
        RESULTS_PATH.read_text(encoding="utf-8")
    )

    baseline = summarize(results, "v1")
    candidate = summarize(results, "v2")

    decision = evaluate_prompt_release(
        candidate=candidate,
        baseline=baseline,
    )

    print("Baseline:", baseline)
    print("Candidate:", candidate)

    print("\nRelease decision:")
    print("APPROVED" if decision.approved else "REJECTED")

    for reason in decision.reasons:
        print(" -", reason)


if __name__ == "__main__":
    main()
