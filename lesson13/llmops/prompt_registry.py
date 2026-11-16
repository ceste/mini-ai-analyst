import hashlib
from dataclasses import dataclass
from pathlib import Path


PROMPT_DIR = Path(__file__).resolve().parent / "prompts"

PROMPT_FILES = {
    "v1": "analyst_v1.txt",
    "v2": "analyst_v2.txt",
}


@dataclass(frozen=True)
class PromptVersion:
    version: str
    content: str
    sha256: str


def load_prompt(version: str) -> PromptVersion:
    if version not in PROMPT_FILES:
        raise ValueError(f"Unknown prompt version: {version}")

    path = PROMPT_DIR / PROMPT_FILES[version]
    content = path.read_text(encoding="utf-8")

    digest = hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()

    return PromptVersion(
        version=version,
        content=content,
        sha256=digest,
    )


if __name__ == "__main__":
    for version in PROMPT_FILES:
        prompt = load_prompt(version)

        print(f"\nVersion: {prompt.version}")
        print(f"SHA256: {prompt.sha256}")
        print(f"Content:\n{prompt.content}")
