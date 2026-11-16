import hashlib

import pytest

from lesson13.llmops.prompt_registry import (
    PROMPT_FILES,
    load_prompt,
)


@pytest.mark.parametrize("version", ["v1", "v2"])
def test_prompt_loads(version):
    prompt = load_prompt(version)

    assert prompt.version == version
    assert prompt.content.strip()


@pytest.mark.parametrize("version", ["v1", "v2"])
def test_prompt_hash_matches_content(version):
    prompt = load_prompt(version)

    expected = hashlib.sha256(
        prompt.content.encode("utf-8")
    ).hexdigest()

    assert prompt.sha256 == expected


def test_prompt_versions_are_distinct():
    v1 = load_prompt("v1")
    v2 = load_prompt("v2")

    assert v1.sha256 != v2.sha256


def test_unknown_prompt_rejected():
    with pytest.raises(ValueError):
        load_prompt("unknown")


def test_registry_files_exist():
    for version in PROMPT_FILES:
        assert load_prompt(version).content
