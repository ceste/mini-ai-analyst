import argparse
import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import httpx

from lesson13.llmops.prompt_registry import load_prompt


OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen2.5:7b"

TRACE_DIR = Path(__file__).resolve().parent / "traces"
TRACE_DIR.mkdir(parents=True, exist_ok=True)

TRACE_FILE = TRACE_DIR / "llm_traces.jsonl"


def run_llm(question: str, prompt_version: str) -> dict:
    prompt = load_prompt(prompt_version)

    trace_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    trace = {
        "trace_id": trace_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": MODEL,
        "prompt_version": prompt.version,
        "prompt_sha256": prompt.sha256,
        "question": question,
        "response": None,
        "latency_ms": None,
        "input_tokens": None,
        "output_tokens": None,
        "ollama_duration_ms": None,
        "status": "error",
        "error": None,
    }

    try:
        with httpx.Client(timeout=120.0) as client:
            response = client.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "stream": False,
                    "messages": [
                        {
                            "role": "system",
                            "content": prompt.content,
                        },
                        {
                            "role": "user",
                            "content": question,
                        },
                    ],
                    "options": {
                        "temperature": 0,
                        "seed": 42,
                    },
                },
            )

            response.raise_for_status()
            data = response.json()

        trace["response"] = data["message"]["content"]
        trace["input_tokens"] = data.get("prompt_eval_count")
        trace["output_tokens"] = data.get("eval_count")

        # Ollama reports duration in nanoseconds.
        if data.get("total_duration") is not None:
            trace["ollama_duration_ms"] = round(
                data["total_duration"] / 1_000_000,
                2,
            )

        trace["status"] = "success"

    except (httpx.HTTPError, KeyError, ValueError) as exc:
        trace["error"] = str(exc)

    finally:
        trace["latency_ms"] = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

        with TRACE_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(trace, ensure_ascii=False) + "\n")

    return trace


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--prompt-version",
        choices=["v1", "v2"],
        required=True,
    )

    parser.add_argument(
        "--question",
        required=True,
    )

    args = parser.parse_args()

    trace = run_llm(
        question=args.question,
        prompt_version=args.prompt_version,
    )

    print(json.dumps(trace, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
