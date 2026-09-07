import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import tempfile
import unittest


spec = importlib.util.spec_from_file_location(
    "freshness", Path(__file__).parents[1] / "helpers/check_repo_freshness.py"
)
freshness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(freshness)


class FreshnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git("init", "-b", "main")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test")
        self.git("config", "commit.gpgsign", "false")
        self.git("commit", "--allow-empty", "-m", "base")
        for remote in ("origin", "fork"):
            self.git("update-ref", f"refs/remotes/{remote}/main", "HEAD")

    def git(self, *args):
        return subprocess.check_output(
            ["git", "-C", str(self.repo), *args], stderr=subprocess.STDOUT
        )

    def check(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return freshness.check(self.repo)

    def test_local_fork_commits_are_current_when_backed_up(self):
        self.git("commit", "--allow-empty", "-m", "local customization")
        self.git("update-ref", "refs/remotes/fork/main", "HEAD")
        self.assertEqual(self.check(), [])

    def test_upstream_divergence_requires_merge(self):
        self.git("checkout", "-b", "upstream")
        self.git("commit", "--allow-empty", "-m", "upstream fix")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")
        self.git("checkout", "main")
        self.git("commit", "--allow-empty", "-m", "local fix")
        self.assertTrue(any("Integrate origin/main" in p for p in self.check()))

    def test_unpushed_commits_require_backup(self):
        self.git("commit", "--allow-empty", "-m", "local fix")
        self.assertTrue(any("git push fork main" in p for p in self.check()))

    def test_dirty_tree_and_feature_branch_fail(self):
        self.git("checkout", "-b", "feature")
        (self.repo / "untracked.txt").write_text("work")
        problems = self.check()
        self.assertTrue(any("Switch to main" in p for p in problems))
        self.assertTrue(any("dirty" in p for p in problems))
