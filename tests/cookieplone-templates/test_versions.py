"""Test the repository-level version pins declared in ``cookieplone-config.json``."""

import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parents[2]
CONFIG_FILE = REPO_ROOT / "cookieplone-config.json"
TEMPLATES_FOLDER = REPO_ROOT / "templates"
WORKFLOWS_FOLDER = REPO_ROOT / ".github/workflows"

# ``frontend_pnpm`` is still consumed through the ``__version_pnpm`` computed
# property, which hardcodes the value.  A ``cookieplone.json`` schema default
# cannot read ``versions``: the wizard renders defaults through tui_forms with a
# ``{"cookiecutter": answers}`` payload only, so ``{{ versions.x }}`` there
# raises ``UndefinedError``.  Centralizing it means moving the reference into
# each consuming file, tracked separately from this test.
KNOWN_UNREFERENCED = {"frontend_pnpm"}

# Actions pinned in this repository's own workflows that also have a pin in
# ``config.versions``.  Actions with no corresponding pin (``setup-uv``,
# ``lychee-action``) are intentionally out of scope.
ACTION_TO_KEY = {
    "actions/cache": "gha_version_cache",
    "actions/checkout": "gha_version_checkout",
    "actions/setup-node": "gha_version_setup_node",
    "JarvusInnovations/background-action": "gha_version_background_action",
}

USES_PATTERN = re.compile(r"uses:\s*([\w.-]+/[\w./-]+)@([\w.-]+)")


@pytest.fixture(scope="module")
def versions() -> dict[str, str]:
    """Return the ``config.versions`` mapping from the repository config.

    :returns: Mapping of pin name to pinned value.
    """
    data = json.loads(CONFIG_FILE.read_text())
    return data["config"]["versions"]


@pytest.fixture(scope="module")
def templates_text() -> str:
    """Concatenate every template file so pin references can be searched.

    :returns: The text of all files under ``templates/``.
    """
    parts: list[str] = []
    for path in sorted(TEMPLATES_FOLDER.rglob("*")):
        if not path.is_file():
            continue
        parts.append(path.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(parts)


def _is_referenced(key: str, text: str) -> bool:
    """Report whether *key* is consumed by a template file or a hook.

    Template files read pins as ``{{ versions.<key> }}``; Python hooks read them
    as ``versions["<key>"]``.

    :param key: The ``config.versions`` key to look for.
    :param text: Concatenated text of every template file.
    :returns: ``True`` when at least one reference exists.
    """
    candidates = (f"versions.{key}", f'versions["{key}"]', f"versions['{key}']")
    return any(candidate in text for candidate in candidates)


def test_every_version_pin_is_consumed(versions, templates_text) -> None:
    """Every pin in ``config.versions`` must be read by a template or hook.

    A pin that nothing references is dead weight: bumping it silently changes
    nothing in the generated project.
    """
    unreferenced = {key for key in versions if not _is_referenced(key, templates_text)}
    unexpected = unreferenced - KNOWN_UNREFERENCED
    assert not unexpected, (
        "These config.versions pins are not read by any template or hook, so "
        f"bumping them would have no effect: {sorted(unexpected)}"
    )


def test_known_unreferenced_pins_are_still_unreferenced(
    versions, templates_text
) -> None:
    """Keep :data:`KNOWN_UNREFERENCED` honest.

    Once a pin is wired up, it must be removed from the exemption set so the
    allowlist cannot quietly rot into a blanket excuse.
    """
    stale = {
        key
        for key in KNOWN_UNREFERENCED
        if key in versions and _is_referenced(key, templates_text)
    }
    assert not stale, (
        f"These pins are now referenced and must be removed from "
        f"KNOWN_UNREFERENCED: {sorted(stale)}"
    )


def test_repository_workflows_match_version_pins(versions) -> None:
    """This repository's own workflows must use the versions it ships.

    The templates hand generated projects the pins from ``config.versions``; if
    this repository's CI drifts from them, it is testing a different toolchain
    than the one its users receive.
    """
    workflows = sorted(WORKFLOWS_FOLDER.glob("*.yml"))
    assert workflows, f"No workflows found in {WORKFLOWS_FOLDER}"

    seen: set[str] = set()
    mismatches: list[str] = []
    for path in workflows:
        for action, ref in USES_PATTERN.findall(path.read_text()):
            seen.add(action)
            key = ACTION_TO_KEY.get(action)
            if key is None:
                continue
            expected = versions[key]
            if ref != expected:
                mismatches.append(
                    f"{path.name}: {action}@{ref} but config.versions.{key} "
                    f"is {expected}"
                )

    missing = set(ACTION_TO_KEY) - seen
    assert not missing, (
        "These actions are no longer used by any workflow, so the drift check "
        f"silently covers nothing — update ACTION_TO_KEY: {sorted(missing)}"
    )
    assert not mismatches, "Workflow pins drifted from config.versions:\n" + "\n".join(
        mismatches
    )
