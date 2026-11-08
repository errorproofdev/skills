#!/usr/bin/env python3
"""Conservative vendored-skill maintenance. Standard library only."""
import argparse
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

CLI = ["npx", "--yes", "skills@1.7.6"]
EXCLUDED = {".DS_Store", ".git", "node_modules", ".venv", "__pycache__"}


def run(args, cwd, capture=False):
    return subprocess.run(args, cwd=cwd, check=True, text=True,
                          stdout=subprocess.PIPE if capture else None,
                          stdin=subprocess.DEVNULL, timeout=600).stdout


def load(path):
    return json.loads(path.read_text())


def save(path, value):
    content = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if path.exists() and load(path) == value:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content)
    temporary.replace(path)


def safe(root, relative):
    parts = Path(relative).parts
    if not parts or Path(relative).is_absolute() or ".." in parts:
        raise ValueError("Unsafe path: " + relative)
    path = root
    for part in parts:
        path = path / part
        if path.is_symlink():
            raise ValueError("Symlink rejected: " + str(path))
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("Path escapes root")
    return path


def snapshot(directory):
    if not directory.is_dir() or directory.is_symlink():
        raise ValueError("Missing or linked skill: " + str(directory))
    result = {}
    for path in sorted(directory.rglob("*")):
        relative = path.relative_to(directory)
        if any(p in EXCLUDED for p in relative.parts):
            continue
        if path.is_symlink():
            raise ValueError("Symlink rejected: " + str(path))
        if path.is_file():
            result[relative.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def skill_name(directory):
    text = (directory / "SKILL.md").read_text()
    if not text.startswith("---\n"):
        raise ValueError("Missing frontmatter: " + str(directory))
    front = text.split("---", 2)[1]
    found = re.search(r"^name:\s*['\"]?([a-z0-9-]+)['\"]?\s*$", front, re.M)
    if not found or not re.search(r"^description:\s*\S", front, re.M):
        raise ValueError("Invalid name/description: " + str(directory))
    return found.group(1)


def dirty(root, path):
    return bool(run(["git", "status", "--porcelain", "--", path], root, True).strip())


def mappings(root):
    data = load(root / "maintenance/sources.json")
    destinations = set()
    for name, entry in data["skills"].items():
        if not re.fullmatch(r"[a-z0-9-]+", name):
            raise ValueError("Invalid skill name")
        expected = re.fullmatch(r"plugins/([a-z0-9-]+)/skills/" + re.escape(name),
                                entry["destination"])
        if not expected or entry["destination"] in destinations:
            raise ValueError("Invalid or duplicate destination")
        destinations.add(entry["destination"])
        safe(root, entry["destination"])
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", entry["source"]):
            raise ValueError("Only explicit GitHub owner/repo sources supported")
        safe(root, entry["skillPath"])
    return data["skills"]


def bootstrap(root, global_lock):
    """Import provenance candidates; seed current upstream without replacing curated files."""
    work = root / "maintenance"
    work.mkdir(exist_ok=True)
    source_file = work / "sources.json"
    if source_file.exists() or (work / "baseline.json").exists():
        raise ValueError("Bootstrap already exists; do not overwrite established baselines")
    candidates = {}
    installed = load(global_lock)["skills"]
    for p in sorted(root.glob("plugins/*/skills/*/SKILL.md")):
        name = p.parent.name
        entry = installed.get(name, {})
        if entry.get("sourceType") == "github" and entry.get("skillPath"):
            candidates[name] = {"source": entry["source"], "skillPath": entry["skillPath"],
                                "destination": p.parent.relative_to(root).as_posix()}
    save(source_file, {"version": 1, "skills": candidates})
    mappings(root)  # Validate before using any source as a command argument.
    groups = {}
    for name, entry in candidates.items():
        groups.setdefault(entry["source"], []).append(name)
    errors = []
    for source, names in groups.items():
        try:
            run(CLI + ["add", source, "--skill"] + names +
                ["-a", "replit", "--copy", "--yes"], work)
        except subprocess.SubprocessError:
            errors.append(source)
    lock = load(work / "skills-lock.json") if (work / "skills-lock.json").exists() else {"skills": {}}
    verified, baseline, skipped = {}, {}, []
    for name, entry in candidates.items():
        p = work / ".agents/skills" / name
        actual = lock["skills"].get(name, {})
        try:
            if (actual.get("source") != entry["source"] or
                    actual.get("skillPath") != entry["skillPath"] or skill_name(p) != name):
                raise ValueError("Provenance does not match")
            baseline[name] = snapshot(p)
            verified[name] = entry
        except (ValueError, OSError):
            skipped.append(name)
    # Only verified entries participate in subsequent CLI updates.
    lock["skills"] = {n: lock["skills"][n] for n in verified}
    save(work / "skills-lock.json", lock)
    save(source_file, {"version": 1, "skills": verified})
    save(work / "baseline.json", baseline)
    save(work / "bootstrap-report.json", {"verified": sorted(verified),
         "unverified": skipped, "failedSources": errors,
         "note": "Name/path provenance verified; existing differences are preserved as local customizations."})
    print(json.dumps({"verified": len(verified), "unverified": len(skipped),
                      "failedSources": errors}))
    if not verified:
        raise ValueError("No sources verified; maintenance is not ready")


def sync(root):
    work = root / "maintenance"
    entries = mappings(root)
    if not entries:
        raise ValueError("No verified upstream mappings")
    baseline = load(work / "baseline.json")
    lock = load(work / "skills-lock.json")["skills"]
    operations, changed, conflicts = [], [], []
    next_base = dict(baseline)
    for name, entry in entries.items():
        dest = safe(root, entry["destination"])
        upstream = safe(work, ".agents/skills/" + name)
        locked = lock.get(name, {})
        if locked.get("source") != entry["source"] or locked.get("skillPath") != entry["skillPath"]:
            raise ValueError("Upstream provenance changed: " + name)
        if skill_name(upstream) != name or skill_name(dest) != name:
            raise ValueError("Skill name mismatch: " + name)
        if dirty(root, entry["destination"]):
            conflicts.append(name + ": uncommitted changes")
            continue
        old = baseline[name]
        new, local = snapshot(upstream), snapshot(dest)
        pending = []
        for relative in sorted(set(old) | set(new)):
            safe(dest, relative)
            if old.get(relative) == new.get(relative):
                continue
            if local.get(relative) not in (old.get(relative), new.get(relative)):
                conflicts.append(name + "/" + relative + ": customization conflict")
                continue
            if local.get(relative) != new.get(relative):
                pending.append((dest, upstream, relative, relative in new))
        operations.extend(pending)
        if pending:
            changed.append(name)
        next_base[name] = new
    if conflicts:
        raise ValueError("Sync blocked; nothing applied:\n" + "\n".join(conflicts))
    for dest, upstream, relative, exists in operations:
        target = safe(dest, relative)
        if exists:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(safe(upstream, relative), target)
        else:
            target.unlink()
    save(work / "baseline.json", next_base)
    print(json.dumps({"updated": changed, "files": len(operations)}))
    return changed


def weekly(root, publish):
    entries = mappings(root)
    for name in ["sources.json", "baseline.json", "skills-lock.json"]:
        if dirty(root, "maintenance/" + name):
            raise ValueError("Commit maintenance setup/state before weekly runs: " + name)
    if publish:
        if run(["git", "branch", "--show-current"], root, True).strip() != "main":
            raise ValueError("Automatic publication is restricted to main")
        url = run(["git", "remote", "get-url", "--push", "origin"], root, True).strip()
        if url not in ("https://github.com/errorproofdev/skills.git",
                       "git@github.com:errorproofdev/skills.git"):
            raise ValueError("Unexpected publication remote")
        run(["git", "fetch", "origin", "main"], root)
        if run(["git", "rev-parse", "HEAD"], root, True) != run(
                ["git", "rev-parse", "origin/main"], root, True):
            raise ValueError("Branch differs from origin/main; reconcile manually")
    # All CLI writes are confined to this staging project, never global installs.
    run(CLI + ["update", "--project", "--yes"], root / "maintenance")
    changed = sync(root)
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], root)
    run(["claude", "plugin", "validate", "."], root)
    for category in sorted({entries[n]["destination"].split("/")[1] for n in changed}):
        run(["claude", "plugin", "validate", "./plugins/" + category, "--strict"], root)
    paths = [entries[n]["destination"] for n in changed]
    paths += ["maintenance/baseline.json", "maintenance/skills-lock.json"]
    diff = run(["git", "diff", "--name-only", "HEAD", "--"] + paths, root, True)
    if not diff.strip():
        print("No changes; no commit.")
        return
    if publish:
        from datetime import datetime
        from zoneinfo import ZoneInfo
        date = datetime.now(ZoneInfo("America/Los_Angeles")).date().isoformat()
        updated = "\n".join("- " + entries[n]["destination"].removeprefix("plugins/").replace("/skills/", "/")
                            + ": upstream files refreshed" for n in changed)
        message = ("chore(skills): weekly maintenance " + date + "\n\nUpdated:\n" +
                   (updated or "- Upstream tracking metadata only") +
                   "\n\nValidation: maintenance tests; marketplace and changed plugins passed\n")
        # --only excludes all unrelated staged and unstaged work, including deletions.
        run(["git", "add", "--"] + paths, root)
        run(["git", "commit", "--only", "-m", message, "--"] + paths, root)
        run(["git", "push", "origin", "HEAD:main"], root)
        print("Published " + run(["git", "rev-parse", "HEAD"], root, True).strip())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("action", choices=["bootstrap", "sync", "weekly"])
    parser.add_argument("--global-lock", type=Path,
                        default=Path.home() / ".agents/.skill-lock.json")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    root = args.repo.resolve()
    # Git-dir lock avoids overlapping jobs without touching tracked files.
    gitdir = Path(run(["git", "rev-parse", "--absolute-git-dir"], root, True).strip())
    with (gitdir / "skill-maintenance.lock").open("w") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if args.action == "bootstrap":
            bootstrap(root, args.global_lock)
        elif args.action == "sync":
            sync(root)
        else:
            weekly(root, args.publish)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
