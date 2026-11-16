import json
import math
import statistics
from collections import defaultdict
from pathlib import Path


TRACE_FILE = (
    Path(__file__).resolve().parent
    / "traces"
    / "llm_traces.jsonl"
)


def percentile(values, p):
    if not values:
        return None

    values = sorted(values)
    position = (len(values) - 1) * p / 100

    lower = math.floor(position)
    upper = math.ceil(position)

    if lower == upper:
        return values[lower]

    weight = position - lower

    return (
        values[lower] * (1 - weight)
        + values[upper] * weight
    )


def analyze():
    if not TRACE_FILE.exists():
        print("No trace file found.")
        return

    traces = []

    for line in TRACE_FILE.read_text(
        encoding="utf-8"
    ).splitlines():
        if line.strip():
            traces.append(json.loads(line))

    if not traces:
        print("No traces available.")
        return

    grouped = defaultdict(list)

    for trace in traces:
        grouped[trace["prompt_version"]].append(trace)

    print("\nLLM OBSERVABILITY REPORT")
    print("=" * 60)

    for version, records in sorted(grouped.items()):
        successful = [
            r for r in records
            if r["status"] == "success"
        ]

        failed = len(records) - len(successful)

        latencies = [
            r["latency_ms"]
            for r in successful
            if r["latency_ms"] is not None
        ]

        input_tokens = sum(
            r.get("input_tokens") or 0
            for r in successful
        )

        output_tokens = sum(
            r.get("output_tokens") or 0
            for r in successful
        )

        # Approximate throughput from Ollama's
        # reported total request duration.
        durations_seconds = sum(
            (r.get("ollama_duration_ms") or 0) / 1000
            for r in successful
        )

        throughput = (
            output_tokens / durations_seconds
            if durations_seconds > 0
            else 0
        )

        print(f"\nPrompt version: {version}")
        print(f"Total requests: {len(records)}")
        print(f"Successful: {len(successful)}")
        print(f"Failed: {failed}")
        print(f"Error rate: {failed / len(records):.1%}")

        if latencies:
            print(
                f"Mean latency: "
                f"{statistics.mean(latencies):.2f} ms"
            )
            print(
                f"Median latency: "
                f"{statistics.median(latencies):.2f} ms"
            )
            print(
                f"P95 latency: "
                f"{percentile(latencies, 95):.2f} ms"
            )

        print(f"Input tokens: {input_tokens}")
        print(f"Output tokens: {output_tokens}")
        print(
            f"Approx. output throughput: "
            f"{throughput:.2f} tokens/sec"
        )


if __name__ == "__main__":
    analyze()
