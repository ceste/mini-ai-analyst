import json
import re
from pathlib import Path

from lesson13.llmops.trace_llm import run_llm


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "evaluation" / "dataset.json"

UNCERTAINTY_PATTERNS = [
    r"\b(?:don't|do not|cannot|can't)\s+(?:have|know|access|provide|determine)",
    r"\bno access\b",
    r"\bnot available\b",
    r"\b(?:need|require)\s+(?:access to|the|more|actual)\s+data\b",
    r"\b(?:without|lack of)\s+(?:access to\s+)?(?:the\s+)?(?:actual\s+)?data\b",
    r"\b(?:don't|do not)\s+have\s+(?:the\s+)?data\b",
]


def evaluate_response(response: str, test_case: dict) -> dict:
    text = response.lower()

    missing_terms = [
        term
        for term in test_case.get("required_terms", [])
        if not re.search(rf"\b{re.escape(term.lower())}\b", text)
    ]

    forbidden_found = [
        term
        for term in test_case.get("forbidden_terms", [])
        if re.search(rf"\b{re.escape(term.lower())}\b", text)
    ]

    uncertainty_ok = True

    if test_case.get("requires_uncertainty", False):
        uncertainty_ok = any(
            re.search(pattern, text)
            for pattern in UNCERTAINTY_PATTERNS
        )

    passed = (
        not missing_terms
        and not forbidden_found
        and uncertainty_ok
    )

    return {
        "passed": passed,
        "missing_terms": missing_terms,
        "forbidden_found": forbidden_found,
        "uncertainty_ok": uncertainty_ok,
    }


def main():
    dataset = json.loads(
        DATASET_PATH.read_text(encoding="utf-8")
    )

    results = []

    for version in ("v1", "v2"):
        print(f"\nEvaluating prompt {version}")
        print("-" * 50)

        for case in dataset:
            trace = run_llm(
                question=case["question"],
                prompt_version=version,
            )

            if trace["status"] != "success":
                evaluation = {
                    "passed": False,
                    "error": trace["error"],
                }
            else:
                evaluation = evaluate_response(
                    trace["response"],
                    case,
                )

            result = {
                "prompt_version": version,
                "test_id": case["id"],
                "question": case["question"],
                "response": trace["response"],
                "latency_ms": trace["latency_ms"],
                "input_tokens": trace["input_tokens"],
                "output_tokens": trace["output_tokens"],
                **evaluation,
            }

            results.append(result)

            status = "PASS" if evaluation["passed"] else "FAIL"
            print(f"{case['id']}: {status}")

    print("\nEVALUATION SUMMARY")
    print("-" * 50)

    for version in ("v1", "v2"):
        version_results = [
            result for result in results
            if result["prompt_version"] == version
        ]

        passed = sum(
            result["passed"]
            for result in version_results
        )

        total = len(version_results)

        avg_latency = sum(
            result["latency_ms"]
            for result in version_results
        ) / total

        print(
            f"{version}: {passed}/{total} passed "
            f"({passed / total:.0%}), "
            f"avg latency: {avg_latency:.2f} ms"
        )

    output_path = BASE_DIR / "evaluation" / "results.json"
    output_path.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()
