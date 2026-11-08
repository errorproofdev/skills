import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts/maintain-skills.py"


class MaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.dest = self.root / "plugins/test/skills/demo"
        self.stage = self.root / "maintenance/.agents/skills/demo"
        self.dest.mkdir(parents=True)
        self.stage.mkdir(parents=True)
        self.put(self.dest / "SKILL.md", "---\nname: demo\ndescription: Test\n---\n")
        self.put(self.stage / "SKILL.md", (self.dest / "SKILL.md").read_text())
        self.put(self.dest / "guide.txt", "base\n")
        self.put(self.stage / "guide.txt", "base\n")
        self.git("init", "-q")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        self.save("maintenance/sources.json", {"version": 1, "skills": {"demo": {
            "source": "example/repo", "skillPath": "skills/demo/SKILL.md",
            "destination": "plugins/test/skills/demo"}}})
        self.save("maintenance/baseline.json", {"demo": self.hashes(self.stage)})
        self.save("maintenance/skills-lock.json", {"version": 1, "skills": {"demo": {
            "source": "example/repo", "sourceType": "github",
            "skillPath": "skills/demo/SKILL.md", "computedHash": "test"}}})
        self.git("add", ".")
        self.git("commit", "-qm", "initial")

    def put(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value)

    def save(self, path, value):
        self.put(self.root / path, json.dumps(value))

    def hashes(self, directory):
        return {str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in directory.rglob("*") if p.is_file()}

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args], text=True).strip()

    def run_sync(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--repo", str(self.root), "sync"],
                                capture_output=True, text=True)
        self.assertTrue(SCRIPT.exists(), "Maintenance implementation is missing")
        return result

    def test_applies_upstream_change_and_deletion(self):
        self.put(self.stage / "guide.txt", "new\n")
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.dest / "guide.txt").read_text(), "new\n")

    def test_preserves_committed_customization_on_conflict(self):
        self.put(self.dest / "guide.txt", "custom\n")
        self.git("add", ".")
        self.git("commit", "-qm", "customize")
        self.put(self.stage / "guide.txt", "upstream\n")
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.dest / "guide.txt").read_text(), "custom\n")
        self.assertIn("conflict", result.stderr.lower())

    def test_dirty_skill_is_not_overwritten(self):
        self.put(self.dest / "guide.txt", "uncommitted\n")
        self.put(self.stage / "guide.txt", "new\n")
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.dest / "guide.txt").read_text(), "uncommitted\n")

    def test_rejects_path_escape(self):
        self.save("maintenance/sources.json", {"version": 1, "skills": {"demo": {
            "source": "example/repo", "skillPath": "skills/demo/SKILL.md",
            "destination": "../outside"}}})
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)

    def test_rejects_upstream_symlink(self):
        (self.stage / "escape").symlink_to("/etc/hosts")
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.dest / "escape").exists())

    def test_deletes_only_upstream_owned_file(self):
        (self.stage / "guide.txt").unlink()
        self.put(self.dest / "custom.txt", "keep\n")
        self.git("add", ".")
        self.git("commit", "-qm", "custom file")
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.dest / "guide.txt").exists())
        self.assertEqual((self.dest / "custom.txt").read_text(), "keep\n")

    def test_one_conflict_blocks_other_file_updates(self):
        self.put(self.dest / "guide.txt", "custom\n")
        self.git("add", ".")
        self.git("commit", "-qm", "customize")
        self.put(self.stage / "guide.txt", "upstream\n")
        self.put(self.stage / "new.txt", "must not apply\n")
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.dest / "new.txt").exists())

    def test_source_change_blocks_sync(self):
        lock = json.loads((self.root / "maintenance/skills-lock.json").read_text())
        lock["skills"]["demo"]["source"] = "unexpected/repo"
        self.save("maintenance/skills-lock.json", lock)
        self.put(self.stage / "guide.txt", "new\n")
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.dest / "guide.txt").read_text(), "base\n")

    def test_upstream_name_change_blocks_sync(self):
        self.put(self.stage / "SKILL.md", "---\nname: other\ndescription: Other\n---\n")
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)

    def test_noop_leaves_baseline_unchanged(self):
        old = (self.root / "maintenance/baseline.json").read_bytes()
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.root / "maintenance/baseline.json").read_bytes(), old)


if __name__ == "__main__":
    unittest.main()
