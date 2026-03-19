import sys
from datetime import date, datetime, timezone
from pathlib import Path

import requests
from repoplone.utils import _git as git
from repoplone.utils import _github as gh
from repoplone.utils import changelog


def sanity_github(session: requests.Session, origin: str) -> bool:
    """Check that the GitHub session and repository are accessible.

    :param session: An authenticated requests.Session with a valid GitHub token.
    :param origin: The remote URL of the repository (e.g. git@github.com:org/repo.git).
    :returns: True if the GitHub API responds successfully for the repository,
        False otherwise.
    :rtype: bool
    """
    status = False
    remote_path = gh._get_owner_repo(origin)
    if session:
        response = session.get(f"https://api.github.com/repos/{remote_path}/releases")
        status = response.status_code == 200
    return status


def create_release(
    session: requests.Session,
    origin: str,
    release_changelog: str,
    version: str,
) -> str:
    """Create a GitHub release for the given version.

    :param session: An authenticated requests.Session with a valid GitHub token.
    :param origin: The remote URL of the repository (e.g. git@github.com:org/repo.git).
    :param release_changelog: Markdown-formatted changelog body for the release.
    :param version: The version string to use as the tag name and release title.
    :returns: A message describing the outcome
        (success with URL, or failure with details).
    :rtype: str
    """
    remote_path = gh._get_owner_repo(origin)
    payload = {
        "tag_name": version,
        "target_commitish": "main",
        "name": version,
        "body": release_changelog,
        "draft": False,
        "prerelease": False,
        "generate_release_notes": False,
    }
    response = session.post(
        f"https://api.github.com/repos/{remote_path}/releases", json=payload
    )
    if response.status_code == 201:
        data = response.json()
        url = data.get("html_url")
        msg = f"Release {version} created at {url}"
    else:
        data = response.json()
        msg = (
            f"Release {version} failed to be created "
            f"({response.status_code} {data['message']})"
        )
    return msg


def next_version(counter: int) -> str:
    """Generate a CalVer version string for today with a sequential counter.

    :param counter: A positive integer disambiguating multiple releases on the same day.
    :returns: A version string in the format ``YYYYMMDD.<counter>``
        (e.g. ``20260319.1``).
    :rtype: str
    """
    today: date = datetime.now(timezone.utc).today()
    return f"{today:%Y%m%d}.{counter}"


def generate_changelog(config: Path, version: str, draft: bool = True) -> str:
    """Run towncrier to produce the changelog for a given version.

    :param config: Path to ``pyproject.toml`` used as the towncrier configuration file.
    :param version: The version string to inject into the changelog.
    :param draft: If ``True``, produce a preview without modifying any files.
    :returns: The generated changelog text.
    :rtype: str
    """
    return changelog._run_towncrier(
        config=config, name="", version=version, draft=draft
    )


def main(dry_run: bool = True) -> None:
    """Orchestrate the release process for the current repository.

    Determines the next CalVer tag, previews the changelog, and — when not in
    dry-run mode — commits the changelog update, pushes the tag, and creates the
    corresponding GitHub release.

    :param dry_run: If ``True`` (default), only preview the changelog and exit
        without making any changes. Pass ``False`` to perform the actual release.
    """
    cwd = Path().cwd()
    pyproject = cwd / "pyproject.toml"

    repo = git.repo_for_project(cwd)
    if not (origin := git._get_remote(repo)):
        # Has no remote
        return

    session = gh.gh_session()
    if not (session and sanity_github(session, origin.url)):
        print("❌ GITHUB_TOKEN not configured or incorrect remote")
        return

    origin.fetch()
    all_tags: list[str] = [tag.name for tag in repo.tags]

    counter = 1
    tag = ""
    while not tag:
        tag = next_version(counter)
        if tag in all_tags:
            tag = ""
            counter += 1
    print(f"🔖 Next version: {tag}\n")
    # Draft changelog
    print("📋 Changelog preview")
    print("─" * 50)
    print(generate_changelog(pyproject, tag, True))
    if not dry_run:
        input("Press Enter to proceed with the release: ")
        print(f"\n🚀 Releasing {tag}...")
        # Generate changelog
        release_changelog = generate_changelog(pyproject, tag, False)
        print("  ✅ Changelog generated")
        # Commit any changes
        git.finish_release(repo, tag)
        print("  ✅ Changes committed and pushed")
        msg = create_release(session, origin.name, release_changelog, tag)
        print(f"  ✅ {msg}")
    else:
        print("👋 Dry run complete — no changes were made.")


if __name__ == "__main__":
    args = sys.argv
    params = args[1:]
    dry_run = "dry-run" in params
    main(dry_run)
