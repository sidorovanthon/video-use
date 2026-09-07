"""Fetch both remotes and verify the working copy is ready for editing.

Run from any directory: python helpers/check_repo_freshness.py
This checks only; merging and pushing remain explicit workflow steps.
"""

from pathlib import Path
import subprocess
import sys


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), *args], text=True, encoding="utf-8"
    ).strip()


def check(repo: Path) -> list[str]:
    problems = []
    if git(repo, "branch", "--show-current") != "main":
        problems.append("Switch to main before editing videos.")
    if git(repo, "status", "--porcelain"):
        problems.append("Working tree is dirty; review and commit or park the changes.")
    for ref in ("origin/main", "fork/main"):
        ahead, behind = map(int, git(
            repo, "rev-list", "--left-right", "--count", f"HEAD...{ref}"
        ).split())
        print(f"{ref}: {ahead} local-only, {behind} remote-only commit(s)")
        if behind:
            problems.append(f"Integrate {ref} with git merge {ref}, then test and commit.")
        if ref == "fork/main" and ahead:
            problems.append("Back up the verified main with git push fork main.")
    return problems


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    try:
        for remote in ("origin", "fork"):
            git(repo, "fetch", remote)
        problems = check(repo)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"Freshness check failed: {exc}", file=sys.stderr)
        return 1
    for problem in problems:
        print(f"FAIL: {problem}")
    if not problems:
        print("PASS: clean main contains origin/main and matches fork/main.")
    return int(bool(problems))


if __name__ == "__main__":
    sys.exit(main())
