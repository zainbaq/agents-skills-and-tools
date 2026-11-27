#!/usr/bin/env python3
"""Lint every pod skill against the repository's layout and frontmatter rules.

usage: python scripts/lint_skills.py [REPO_ROOT]

Exits 1 if any rule is broken, 0 otherwise. Standard library only.

Checked for every plugins/<pod>/skills/<skill>/SKILL.md:
  - frontmatter exists and has exactly the keys `name` and `description`
  - name: lowercase letters, digits and hyphens, at most 64 characters, equal to the folder name
  - description: non-empty, at most 1,024 characters, not written as "Use when ..." or in first/second person
  - body has the headings `## Inputs`, `## Process`, `## Outputs`, in that order
  - file is at most 500 lines
  - no Python script is embedded in the file (scripts live in scripts/)
  - every referenced script and every relative link exists, inside the pod
Checked for the repository:
  - no SKILL.md outside archive/ and plugins/
  - every pod's plugin.json name equals its folder name and its marketplace.json entry
"""
import json
import re
import sys
from pathlib import Path

ALLOWED_KEYS = {"name", "description"}
REQUIRED_HEADINGS = ["Inputs", "Process", "Outputs"]
MAX_LINES = 500
MAX_NAME = 64
MAX_DESCRIPTION = 1024
NAME_RE = re.compile(r"^[a-z0-9-]+$")
SCRIPT_REF_RE = re.compile(r"(?<![\w./-])((?:\.\./[\w-]+/)?scripts/[\w.-]+\.[A-Za-z0-9]+)")
LINK_RE = re.compile(r"\]\(([^)\s#]+)(?:#[^)]*)?\)")
BAD_DESCRIPTION_START = re.compile(r"^(use (this|when|whenever|for)\b|i |i'|you |your )", re.I)
SKIP_DIRS = {".git", "node_modules", "__pycache__"}


def split_frontmatter(text):
    """Return (frontmatter_lines, body_lines) or (None, all_lines) when there is no frontmatter."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, lines
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], lines[i + 1:]
    return None, lines


def parse_frontmatter(fm_lines):
    """Parse top-level `key: value` pairs. Indented and continuation lines join the previous value."""
    data, key = {}, None
    for raw in fm_lines:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", raw)
        if m and not raw[0].isspace():
            key, value = m.group(1), m.group(2).strip()
            data[key] = value
        elif key is not None:
            data[key] = (data[key] + " " + raw.strip()).strip()
    for k, v in data.items():
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
            v = v.replace('\\"', '"') if data[k][0] == '"' else v.replace("''", "'")
        elif v in (">", "|", ">-", "|-"):
            v = ""
        data[k] = v
    return data


def strip_fences(lines):
    """Yield (line, in_fence, fence_lang) so headings inside code blocks are ignored."""
    in_fence, lang = False, ""
    for line in lines:
        s = line.strip()
        if s.startswith("```"):
            if not in_fence:
                in_fence, lang = True, s[3:].strip().lower()
            else:
                in_fence, lang = False, ""
            yield line, True, lang
            continue
        yield line, in_fence, lang


def lint_skill(skill_dir, pod_dir):
    errors = []
    path = skill_dir / "SKILL.md"
    if not path.is_file():
        return [f"{skill_dir}: no SKILL.md"]
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    n_lines = len(text.rstrip("\n").split("\n"))
    if n_lines > MAX_LINES:
        errors.append(f"{n_lines} lines, limit {MAX_LINES}")

    fm_lines, body = split_frontmatter(text)
    if fm_lines is None:
        errors.append("no frontmatter block")
        fm = {}
    else:
        fm = parse_frontmatter(fm_lines)
        extra = sorted(set(fm) - ALLOWED_KEYS)
        missing = sorted(ALLOWED_KEYS - set(fm))
        if extra:
            errors.append(f"frontmatter keys not allowed: {', '.join(extra)}")
        if missing:
            errors.append(f"frontmatter keys missing: {', '.join(missing)}")

    name = fm.get("name", "")
    if name:
        if not NAME_RE.match(name):
            errors.append(f'name "{name}" must be lowercase letters, digits and hyphens')
        if len(name) > MAX_NAME:
            errors.append(f"name is {len(name)} characters, limit {MAX_NAME}")
        if name != skill_dir.name:
            errors.append(f'name "{name}" does not match folder "{skill_dir.name}"')

    desc = fm.get("description", "")
    if "description" in fm:
        if not desc.strip():
            errors.append("description is empty")
        if len(desc) > MAX_DESCRIPTION:
            errors.append(f"description is {len(desc)} characters, limit {MAX_DESCRIPTION}")
        if BAD_DESCRIPTION_START.match(desc.strip()):
            errors.append("description must be third person and say what the skill does before when to use it")

    headings, python_fences = [], 0
    for line, in_fence, lang in strip_fences(body):
        if in_fence:
            if line.strip().startswith("```") and lang in ("python", "py", "python3"):
                python_fences += 1
            continue
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            headings.append(m.group(1))
    positions = []
    for h in REQUIRED_HEADINGS:
        if h not in headings:
            errors.append(f'missing heading "## {h}"')
        else:
            positions.append(headings.index(h))
    if len(positions) == len(REQUIRED_HEADINGS) and positions != sorted(positions):
        errors.append("headings must come in the order Inputs, Process, Outputs")
    if python_fences:
        errors.append(f"{python_fences} embedded Python block(s); move the code to scripts/")

    body_text = "\n".join(body)
    refs = set(SCRIPT_REF_RE.findall(body_text))
    refs |= {t for t in LINK_RE.findall(body_text) if not re.match(r"^[a-z][a-z0-9+.-]*:", t, re.I)}
    pod_root = pod_dir.resolve()
    for ref in sorted(refs):
        target = (skill_dir / ref).resolve()
        if pod_root != target and pod_root not in target.parents:
            errors.append(f"reference leaves the pod: {ref}")
        elif not target.exists():
            errors.append(f"referenced file does not exist: {ref}")

    scripts_dir = skill_dir / "scripts"
    if scripts_dir.is_dir():
        for f in sorted(scripts_dir.iterdir()):
            if f.is_file() and f"scripts/{f.name}" not in body_text:
                errors.append(f"scripts/{f.name} is never referenced in SKILL.md")
    return [f"{path.as_posix()}: {e}" for e in errors]


def lint_repo(root):
    errors, skills = [], 0
    for p in root.rglob("SKILL.md"):
        rel = p.relative_to(root)
        if SKIP_DIRS & set(rel.parts):
            continue
        if rel.parts[0] not in ("archive", "plugins"):
            errors.append(f"{rel.as_posix()}: SKILL.md is only allowed under archive/ and plugins/")

    entries = {}
    market = root / ".claude-plugin" / "marketplace.json"
    if market.is_file():
        for e in json.loads(market.read_text(encoding="utf-8")).get("plugins", []):
            if isinstance(e.get("source"), str):
                entries[e["source"].rstrip("/")] = e.get("name")
    else:
        errors.append(".claude-plugin/marketplace.json is missing")

    plugins = root / "plugins"
    for pod in sorted(d for d in plugins.iterdir() if d.is_dir()) if plugins.is_dir() else []:
        manifest = pod / ".claude-plugin" / "plugin.json"
        if not manifest.is_file():
            errors.append(f"{pod.relative_to(root).as_posix()}: no .claude-plugin/plugin.json")
        else:
            pname = json.loads(manifest.read_text(encoding="utf-8")).get("name")
            if pname != pod.name:
                errors.append(f'{manifest.relative_to(root).as_posix()}: name "{pname}" does not match folder "{pod.name}"')
            listed = entries.get(f"./plugins/{pod.name}")
            if listed != pname:
                errors.append(f'{pod.name}: marketplace.json entry name "{listed}" does not match plugin.json name "{pname}"')
        skills_dir = pod / "skills"
        for skill in sorted(d for d in skills_dir.iterdir() if d.is_dir()) if skills_dir.is_dir() else []:
            skills += 1
            for e in lint_skill(skill, pod):
                errors.append(e.replace(root.as_posix() + "/", ""))
    return errors, skills


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent).resolve()
    errors, skills = lint_repo(root)
    for e in errors:
        print("ERROR", e)
    print(f"{skills} skill(s) checked, {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
