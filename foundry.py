#!/usr/bin/env python3
"""
DSAI Foundry — Unified Developer CLI & Contribution Engine.

Commands:
  new     Scaffold a new contribution entry from template
  check   Validate an entry or staged files (file sizes, syntax, placeholders, secrets)
  index   Regenerate directory tables across root README, category READMEs, and LEADERBOARD
  hooks   Configure Git to use repository pre-commit hooks (.githooks/)

Zero external dependencies — runs on Python 3.10+ standard library.
"""

from __future__ import annotations

import argparse
import json
import os
import py_compile
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Ensure UTF-8 output even on legacy Windows code pages
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Constants & Configuration
CATEGORIES = ("trained-models", "papers-implemented", "projects")
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
REPO_ROOT = Path(__file__).resolve().parent

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SECRET_PATTERNS = [
    re.compile(r"(sk-[a-zA-Z0-9_-]{20,})"),           # OpenAI API key
    re.compile(r"(gsk_[a-zA-Z0-9_-]{20,})"),          # Groq API key
    re.compile(r"(hf_[a-zA-Z0-9_-]{20,})"),           # Hugging Face token
    re.compile(r"(ghp_[a-zA-Z0-9_-]{20,})"),          # GitHub personal token
    re.compile(r"(AKIA[0-9A-Z]{16})"),                # AWS Access Key ID
]

PLACEHOLDER_MARKERS = [
    "[Paper Title]",
    "[Model Name]",
    "[Project Name]",
    "*Full paper title*",
    "*Author A, Author B, et al.*",
    "*Your Name*",
    "[@your-handle](https://github.com/your-handle)",
    "*Briefly describe what this model does and on what data.*",
    "*Briefly describe what this project does and the problem it solves.*",
]


class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def colorize(text: str, color: str) -> str:
    # Disable color codes if output is not a TTY or on simple terminals
    if not sys.stdout.isatty():
        return text
    return f"{color}{text}{Colors.RESET}"


# ============================================================================
# COMMAND: NEW (Scaffold)
# ============================================================================
def cmd_new(args: argparse.Namespace) -> int:
    """Scaffold a new entry directory from template."""
    print(colorize("\n🚀 DSAI Foundry — Entry Scaffolder\n", Colors.BOLD + Colors.BLUE))

    category = args.category
    while category not in CATEGORIES:
        print("Available categories:")
        for idx, cat in enumerate(CATEGORIES, 1):
            print(f"  [{idx}] {cat}")
        choice = input("Select category (1-3): ").strip()
        if choice in ("1", "2", "3"):
            category = CATEGORIES[int(choice) - 1]
        elif choice in CATEGORIES:
            category = choice
        else:
            print(colorize("Invalid category. Try again.\n", Colors.RED))

    slug = args.slug
    while not slug or not SLUG_PATTERN.match(slug):
        if slug:
            print(colorize("Invalid slug! Must be kebab-case (e.g. resnet50-cifar10).", Colors.RED))
        slug = input("Entry slug (kebab-case, e.g. transformer-scratch): ").strip().lower()

    target_dir = REPO_ROOT / category / slug
    if target_dir.exists():
        print(colorize(f"Error: Target directory already exists: {target_dir}", Colors.RED))
        return 1

    template_dir = REPO_ROOT / category / "_template"
    if not template_dir.exists():
        print(colorize(f"Error: Template directory not found: {template_dir}", Colors.RED))
        return 1

    title = args.title or input("Entry title: ").strip() or slug.replace("-", " ").title()
    author = args.author or input("Your full name: ").strip() or "Anonymous Contributor"
    github = (args.github or input("GitHub handle (without @): ").strip()).lstrip("@") or "contributor"
    summary = args.summary or input("One-line summary: ").strip() or f"Implementation of {title}"
    tags_input = args.tags or input("Tags (comma-separated, e.g. nlp, llm, agents): ").strip()
    tags = [t.strip().lower() for t in tags_input.split(",") if t.strip()]

    # Copy template
    shutil.copytree(template_dir, target_dir)

    # Clean up template .gitkeep files if we have directories
    for keep_file in target_dir.rglob(".gitkeep"):
        try:
            keep_file.unlink()
        except OSError:
            pass

    # Populate README.md
    readme_path = target_dir / "README.md"
    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8")
        content = content.replace("[Paper Title]", title)
        content = content.replace("[Model Name]", title)
        content = content.replace("[Project Name]", title)
        content = content.replace("*Full paper title*", title)
        content = content.replace("*Briefly describe what this model does and on what data.*", summary)
        content = content.replace("*Briefly describe what this project does and the problem it solves.*", summary)
        content = content.replace("*An implementation of \"[Paper Title]\" with reproduced results.*", summary)
        content = content.replace("*Your Name*", author)
        content = content.replace("[@your-handle](https://github.com/your-handle)", f"[@{github}](https://github.com/{github})")
        content = content.replace("@your-handle", f"@{github}")
        readme_path.write_text(content, encoding="utf-8")

    # Write entry.json metadata
    entry_meta = {
        "title": title,
        "slug": slug,
        "category": category,
        "author": author,
        "github": github,
        "summary": summary,
        "tags": tags,
        "paper_url": args.paper_url or "",
        "created_at": "2026-09-19",
    }
    (target_dir / "entry.json").write_text(json.dumps(entry_meta, indent=2), encoding="utf-8")

    # Create starter .env.example
    env_example = target_dir / ".env.example"
    if not env_example.exists():
        env_example.write_text("# Environment variables for this entry\n# KEY=value\n", encoding="utf-8")

    print(colorize(f"\n✓ Successfully scaffolded: {category}/{slug}/", Colors.GREEN + Colors.BOLD))
    print("\nNext steps:")
    print(f"  1. Add your code in: {category}/{slug}/src/")
    print(f"  2. Add your requirements in: {category}/{slug}/requirements.txt")
    print(f"  3. Fill in details in: {category}/{slug}/README.md")
    print(f"  4. Test and validate: python foundry.py check {category}/{slug}")
    print()
    return 0


# ============================================================================
# COMMAND: CHECK (Validation)
# ============================================================================
def get_staged_files() -> list[Path]:
    """Return list of staged files in git."""
    try:
        output = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        return [REPO_ROOT / line.strip() for line in output.splitlines() if line.strip()]
    except (subprocess.SubprocessError, FileNotFoundError):
        return []


def safe_rel_path(path: Path) -> str:
    """Return relative path to REPO_ROOT if possible, else full path."""
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def check_file_sizes(files: list[Path]) -> list[str]:
    """Ensure no file exceeds 10 MB."""
    errors = []
    for file_path in files:
        if file_path.is_file():
            size = file_path.stat().st_size
            if size > MAX_FILE_SIZE_BYTES:
                mb = size / (1024 * 1024)
                errors.append(
                    f"File exceeds 10MB limit ({mb:.2f} MB): {safe_rel_path(file_path)}"
                )
    return errors


def check_secrets(files: list[Path]) -> list[str]:
    """Scan files for committed secrets or .env files."""
    errors = []
    for file_path in files:
        if not file_path.is_file():
            continue
        rel = safe_rel_path(file_path)
        name = file_path.name
        # Disallow real .env files
        if name == ".env" or (name.startswith(".env.") and not name.endswith(".example")):
            errors.append(f"Do not commit active environment files: {rel}")
            continue

        # Skip example config files from secret regex scanning
        if name.endswith(".example"):
            continue

        # Skip scanning binaries, git, notebooks, or images for regex
        if file_path.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".pyc", ".ipynb"):
            continue

        try:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
            for pattern in SECRET_PATTERNS:
                for match in pattern.finditer(text):
                    val = match.group(0).lower()
                    # Ignore obvious placeholders
                    if any(dummy in val for dummy in ("your", "here", "dummy", "example", "placeholder", "xxx", "token")):
                        continue
                    masked = match.group(0)[:6] + "..." + match.group(0)[-4:]
                    errors.append(f"Potential secret detected ({masked}) in: {rel}")
                    break
        except Exception:
            pass
    return errors


def check_python_syntax(files: list[Path]) -> list[str]:
    """Run py_compile on all python files."""
    errors = []
    py_files = [f for f in files if f.is_file() and f.suffix == ".py"]
    for py_file in py_files:
        try:
            py_compile.compile(str(py_file), doraise=True)
        except py_compile.PyCompileError as e:
            rel = safe_rel_path(py_file)
            errors.append(f"Python syntax error in {rel}: {e.msg}")
    return errors


def check_entry_structure(entry_dir: Path) -> list[str]:
    """Check structural rules for a single entry directory."""
    errors = []
    rel = entry_dir.relative_to(REPO_ROOT)
    parts = rel.parts

    if len(parts) != 2 or parts[0] not in CATEGORIES:
        return [f"Entry must be directly inside one of {CATEGORIES}: {rel}"]

    slug = parts[1]
    if slug == "_template":
        return []

    if not SLUG_PATTERN.match(slug):
        errors.append(f"Folder name must be kebab-case: {slug}")

    readme = entry_dir / "README.md"
    if not readme.exists():
        errors.append(f"Missing README.md in {rel}")
    else:
        content = readme.read_text(encoding="utf-8", errors="ignore")
        for marker in PLACEHOLDER_MARKERS:
            if marker in content:
                errors.append(f"Unmodified placeholder '{marker}' found in {readme.relative_to(REPO_ROOT)}")

    reqs = entry_dir / "requirements.txt"
    if not reqs.exists():
        errors.append(f"Missing requirements.txt in {rel}")

    return errors


def cmd_check(args: argparse.Namespace) -> int:
    """Validate entry directory or staged files."""
    target_path = Path(args.target).resolve() if args.target else None
    staged_mode = args.staged

    print(colorize("🔍 DSAI Foundry — Pre-flight Validator\n", Colors.BOLD + Colors.BLUE))

    files_to_check: list[Path] = []
    entries_to_check: set[Path] = set()

    if staged_mode:
        files_to_check = get_staged_files()
        if not files_to_check:
            print(colorize("✓ No staged files found to check.", Colors.GREEN))
            return 0
        for f in files_to_check:
            try:
                rel = f.relative_to(REPO_ROOT)
                # Only check entry structure if the file belongs to an entry subfolder (len(parts) > 2)
                if len(rel.parts) > 2 and rel.parts[0] in CATEGORIES and rel.parts[1] != "_template":
                    candidate = REPO_ROOT / rel.parts[0] / rel.parts[1]
                    if candidate.is_dir():
                        entries_to_check.add(candidate)
            except ValueError:
                pass
    elif target_path:
        if not target_path.exists():
            print(colorize(f"Error: Target path does not exist: {target_path}", Colors.RED))
            return 1
        if target_path.is_file():
            files_to_check = [target_path]
        else:
            files_to_check = [p for p in target_path.rglob("*") if p.is_file()]
            entries_to_check.add(target_path)
    else:
        # Check all entries in repo
        for cat in CATEGORIES:
            cat_dir = REPO_ROOT / cat
            if cat_dir.exists():
                for sub in cat_dir.iterdir():
                    if sub.is_dir() and sub.name != "_template":
                        entries_to_check.add(sub)
                        files_to_check.extend([p for p in sub.rglob("*") if p.is_file()])

    # Run checks
    all_errors: list[str] = []

    # 1. File size check
    size_errors = check_file_sizes(files_to_check)
    all_errors.extend(size_errors)

    # 2. Secret exposure check
    secret_errors = check_secrets(files_to_check)
    all_errors.extend(secret_errors)

    # 3. Python syntax check
    syntax_errors = check_python_syntax(files_to_check)
    all_errors.extend(syntax_errors)

    # 4. Entry structure & placeholder check
    for entry in entries_to_check:
        structure_errors = check_entry_structure(entry)
        all_errors.extend(structure_errors)

    # Report results
    if all_errors:
        print(colorize(f"❌ Verification failed with {len(all_errors)} issue(s):\n", Colors.RED + Colors.BOLD))
        for err in all_errors:
            print(f"  • {colorize(err, Colors.RED)}")
        print()
        return 1

    print(colorize(f"✓ All checks passed successfully! ({len(files_to_check)} files, {len(entries_to_check)} entries verified)", Colors.GREEN + Colors.BOLD))
    print()
    return 0


# ============================================================================
# COMMAND: INDEX (Directory & Leaderboard Regeneration)
# ============================================================================
def extract_entry_metadata(entry_dir: Path) -> dict:
    """Extract metadata from entry.json or fallback to README.md."""
    meta_file = entry_dir / "entry.json"
    if meta_file.exists():
        try:
            data = json.loads(meta_file.read_text(encoding="utf-8"))
            data["slug"] = entry_dir.name
            data["category"] = entry_dir.parent.name
            return data
        except Exception:
            pass

    # Fallback to parsing README.md
    readme = entry_dir / "README.md"
    title = entry_dir.name.replace("-", " ").title()
    summary = ""
    author = "Club Contributor"
    github = "dsai-iitbhilai"
    paper_url = ""
    tags: list[str] = []

    if readme.exists():
        lines = readme.read_text(encoding="utf-8", errors="ignore").splitlines()
        for idx, line in enumerate(lines):
            line_str = line.strip()
            if line_str.startswith("# ") and title == entry_dir.name.replace("-", " ").title():
                title = line_str.replace("# ", "").split("—")[0].strip()
            if line_str.startswith("> **One-line summary:**"):
                summary = line_str.replace("> **One-line summary:**", "").replace("*", "").strip()
            if "arxiv.org" in line_str and not paper_url:
                match = re.search(r"https?://arxiv\.org/[^\s\)\>]+", line_str)
                if match:
                    paper_url = match.group(0)

    return {
        "title": title,
        "slug": entry_dir.name,
        "category": entry_dir.parent.name,
        "author": author,
        "github": github,
        "summary": summary or f"Implementation of {title}",
        "tags": tags,
        "paper_url": paper_url,
    }


def cmd_index(args: argparse.Namespace) -> int:
    """Regenerate directory tables in READMEs and LEADERBOARD."""
    print(colorize("📋 DSAI Foundry — Index & Leaderboard Builder\n", Colors.BOLD + Colors.BLUE))

    entries_by_cat: dict[str, list[dict]] = {cat: [] for cat in CATEGORIES}
    contributors: dict[str, dict] = {}

    for cat in CATEGORIES:
        cat_dir = REPO_ROOT / cat
        if not cat_dir.exists():
            continue
        for sub in sorted(cat_dir.iterdir()):
            if sub.is_dir() and sub.name != "_template":
                meta = extract_entry_metadata(sub)
                entries_by_cat[cat].append(meta)

                author = meta.get("author", "Contributor")
                gh = meta.get("github", "contributor")
                if gh not in contributors:
                    contributors[gh] = {
                        "name": author,
                        "github": gh,
                        "entries": 0,
                        "categories": set(),
                        "items": [],
                    }
                contributors[gh]["entries"] += 1
                contributors[gh]["categories"].add(cat)
                contributors[gh]["items"].append((cat, meta["slug"], meta["title"]))

def render_root_category_table(category: str, entries: list[dict]) -> str:
    """Render markdown directory table for root README."""
    lines = []
    if category == "papers-implemented":
        lines.append("| Entry | Contributor | Paper | Description |")
        lines.append("|-------|-------------|-------|-------------|")
        for e in entries:
            paper_col = f"[{e.get('paper_title') or 'Paper'}]({e['paper_url']})" if e.get("paper_url") else "—"
            tag_badges = " ".join(f"`{t}`" for t in e.get("tags", []))
            desc = e.get("description") or e.get("summary") or "—"
            if tag_badges:
                desc = f"{desc} <br> {tag_badges}"
            lines.append(f"| [{e['title']}]({category}/{e['slug']}/) | [@{e['github']}](https://github.com/{e['github']}) | {paper_col} | {desc} |")
        lines.append("| *Your entry here* | — | — | [Submit yours →](CONTRIBUTING.md) |")
    else:
        lines.append("| Entry | Contributor | Description |")
        lines.append("|-------|-------------|-------------|")
        for e in entries:
            tag_badges = " ".join(f"`{t}`" for t in e.get("tags", []))
            desc = e.get("description") or e.get("summary") or "—"
            if tag_badges:
                desc = f"{desc} <br> {tag_badges}"
            lines.append(f"| [{e['title']}]({category}/{e['slug']}/) | [@{e['github']}](https://github.com/{e['github']}) | {desc} |")
        lines.append("| *Your entry here* | — | [Submit yours →](CONTRIBUTING.md) |")
    return "\n".join(lines)


def update_root_readme(entries_by_cat: dict[str, list[dict]], check_only: bool = False) -> bool:
    """Update directory tables in root README.md."""
    root_readme = REPO_ROOT / "README.md"
    if not root_readme.exists():
        return True

    content = root_readme.read_text(encoding="utf-8")
    original = content

    # Replace Trained Models table
    pattern_tm = re.compile(r"(### Trained Models\s*\n\n)(?:\|[^\n]+\n)+\n?", re.MULTILINE)
    table_tm = render_root_category_table("trained-models", entries_by_cat.get("trained-models", []))
    content = pattern_tm.sub(f"\\1{table_tm}\n\n", content)

    # Replace Paper Implementations table
    pattern_pi = re.compile(r"(### Paper Implementations\s*\n\n)(?:\|[^\n]+\n)+\n?", re.MULTILINE)
    table_pi = render_root_category_table("papers-implemented", entries_by_cat.get("papers-implemented", []))
    content = pattern_pi.sub(f"\\1{table_pi}\n\n", content)

    # Replace Projects table
    pattern_pr = re.compile(r"(### Projects\s*\n\n)(?:\|[^\n]+\n)+\n?", re.MULTILINE)
    table_pr = render_root_category_table("projects", entries_by_cat.get("projects", []))
    content = pattern_pr.sub(f"\\1{table_pr}\n\n", content)

    if content != original:
        if check_only:
            return False
        root_readme.write_text(content, encoding="utf-8")
    return True


def update_leaderboard(contributors: dict[str, dict], check_only: bool = False) -> bool:
    """Update top contributors table in LEADERBOARD.md."""
    lb_path = REPO_ROOT / "LEADERBOARD.md"
    if not lb_path.exists():
        return True

    content = lb_path.read_text(encoding="utf-8")
    original = content

    # Sort contributors by entries descending
    sorted_contributors = sorted(contributors.values(), key=lambda c: c["entries"], reverse=True)

    lines = [
        "| Rank | Name | GitHub | Entries | Categories |",
        "|------|------|--------|---------|------------|",
    ]
    CAT_DISPLAY = {
        "papers-implemented": "Paper Implementations",
        "trained-models": "Trained Models",
        "projects": "Projects",
    }
    if not sorted_contributors:
        lines.append("| — | *Be the first!* | — | — | — |")
    else:
        for rank, c in enumerate(sorted_contributors, 1):
            cats = ", ".join(CAT_DISPLAY.get(cat, cat.replace("-", " ").title()) for cat in sorted(c["categories"]))
            lines.append(f"| {rank} | {c['name']} | [@{c['github']}](https://github.com/{c['github']}) | {c['entries']} | {cats} |")

    table_text = "\n".join(lines)
    pattern_top = re.compile(r"(## 📊 Top Contributors\s*\n\n)(?:\|[^\n]+\n)+\n?", re.MULTILINE)
    content = pattern_top.sub(f"\\1{table_text}\n\n", content)

    if content != original:
        if check_only:
            return False
        lb_path.write_text(content, encoding="utf-8")
    return True


def cmd_index(args: argparse.Namespace) -> int:
    """Regenerate directory tables in READMEs and LEADERBOARD."""
    check_only = getattr(args, "check", False)
    print(colorize(f"📋 DSAI Foundry — Index & Leaderboard {'Validator' if check_only else 'Builder'}\n", Colors.BOLD + Colors.BLUE))

    entries_by_cat: dict[str, list[dict]] = {cat: [] for cat in CATEGORIES}
    contributors: dict[str, dict] = {}

    for cat in CATEGORIES:
        cat_dir = REPO_ROOT / cat
        if not cat_dir.exists():
            continue
        for sub in sorted(cat_dir.iterdir()):
            if sub.is_dir() and sub.name != "_template":
                meta = extract_entry_metadata(sub)
                entries_by_cat[cat].append(meta)

                author = meta.get("author", "Contributor")
                gh = meta.get("github", "contributor")
                if gh not in contributors:
                    contributors[gh] = {
                        "name": author,
                        "github": gh,
                        "entries": 0,
                        "categories": set(),
                        "items": [],
                    }
                contributors[gh]["entries"] += 1
                contributors[gh]["categories"].add(cat)
                contributors[gh]["items"].append((cat, meta["slug"], meta["title"]))

    needs_update = False

    # 1. Update category READMEs
    for cat in CATEGORIES:
        cat_readme = REPO_ROOT / cat / "README.md"
        if not cat_readme.exists():
            continue
        cat_entries = entries_by_cat[cat]
        lines = cat_readme.read_text(encoding="utf-8").splitlines()
        new_lines = []

        for line in lines:
            if line.strip().startswith("## Entries"):
                new_lines.append("## Entries\n")
                if not cat_entries:
                    new_lines.append("*No entries yet — be the first to contribute! 🚀*\n")
                else:
                    if cat == "papers-implemented":
                        new_lines.append("| Entry | Paper | Contributor | Description |")
                        new_lines.append("|-------|-------|-------------|-------------|")
                        for e in cat_entries:
                            paper_link = f"[Paper]({e['paper_url']})" if e.get("paper_url") else "—"
                            new_lines.append(f"| [{e['title']}]({e['slug']}/) | {paper_link} | [@{e['github']}](https://github.com/{e['github']}) | {e.get('description') or e.get('summary')} |")
                        new_lines.append("| *Your entry here* | — | — | [Submit yours →](../CONTRIBUTING.md) |")
                    else:
                        new_lines.append("| Entry | Contributor | Description |")
                        new_lines.append("|-------|-------------|-------------|")
                        for e in cat_entries:
                            new_lines.append(f"| [{e['title']}]({e['slug']}/) | [@{e['github']}](https://github.com/{e['github']}) | {e.get('description') or e.get('summary')} |")
                        new_lines.append("| *Your entry here* | — | [Submit yours →](../CONTRIBUTING.md) |")
                break
            else:
                new_lines.append(line)

        new_content = "\n".join(new_lines) + "\n"
        orig_content = cat_readme.read_text(encoding="utf-8")
        if new_content != orig_content:
            if check_only:
                needs_update = True
            else:
                cat_readme.write_text(new_content, encoding="utf-8")
        print(f"  • Checked: {cat}/README.md ({len(cat_entries)} entries)")

    # 2. Update root README
    root_ok = update_root_readme(entries_by_cat, check_only=check_only)
    if not root_ok:
        needs_update = True
    print(f"  • Checked: root README.md directory tables")

    # 3. Update LEADERBOARD
    lb_ok = update_leaderboard(contributors, check_only=check_only)
    if not lb_ok:
        needs_update = True
    print(f"  • Checked: LEADERBOARD.md ({len(contributors)} contributors)")

    if check_only and needs_update:
        print(colorize("\n❌ Index tables are out of date! Run `python foundry.py index` to regenerate.", Colors.RED + Colors.BOLD))
        return 1

    print(colorize(f"\n✓ Indexing {'verified' if check_only else 'complete'}!", Colors.GREEN + Colors.BOLD))
    return 0


# ============================================================================
# COMMAND: HOOKS (Git pre-commit setup)
# ============================================================================
def cmd_hooks(args: argparse.Namespace) -> int:
    """Configure core.hooksPath to point to .githooks/."""
    print(colorize("⚓ DSAI Foundry — Git Hook Setup\n", Colors.BOLD + Colors.BLUE))
    hooks_dir = REPO_ROOT / ".githooks"
    if not hooks_dir.exists():
        hooks_dir.mkdir(parents=True, exist_ok=True)

    try:
        subprocess.check_call(["git", "config", "core.hooksPath", ".githooks"])
        print(colorize("✓ Git configured to use .githooks/ directory!", Colors.GREEN + Colors.BOLD))
        print("Commits will now automatically be checked for:")
        print("  • Files over 10 MB limit")
        print("  • Leaked secret tokens or active .env files")
        print("  • Python syntax compilation errors")
        print("  • Unreplaced template placeholders")
        return 0
    except subprocess.SubprocessError as e:
        print(colorize(f"Error configuring git hooks: {e}", Colors.RED))
        return 1


# ============================================================================
# CLI ENTRYPOINT
# ============================================================================
def main() -> int:
    parser = argparse.ArgumentParser(
        prog="foundry",
        description="DSAI Foundry — Developer CLI & Contribution Workflow Tool",
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Command: new
    parser_new = subparsers.add_parser("new", help="Scaffold a new entry from template")
    parser_new.add_argument("--category", choices=CATEGORIES, help="Category name")
    parser_new.add_argument("--slug", help="Kebab-case entry slug")
    parser_new.add_argument("--title", help="Full entry title")
    parser_new.add_argument("--author", help="Author full name")
    parser_new.add_argument("--github", help="Author GitHub handle")
    parser_new.add_argument("--summary", help="One-line summary")
    parser_new.add_argument("--tags", help="Comma-separated tags")
    parser_new.add_argument("--paper-url", help="Paper URL (if applicable)")

    # Command: check
    parser_check = subparsers.add_parser("check", help="Validate an entry or staged files")
    parser_check.add_argument("target", nargs="?", help="Directory or file to validate")
    parser_check.add_argument("--staged", action="store_true", help="Validate git staged files only")

    # Command: index
    parser_index = subparsers.add_parser("index", help="Regenerate directory tables & leaderboard")
    parser_index.add_argument("--check", action="store_true", help="Check if indexes are up to date without modifying files")

    # Command: hooks
    parser_hooks = subparsers.add_parser("hooks", help="Configure git pre-commit hooks")

    args = parser.parse_args()

    if args.command == "new":
        return cmd_new(args)
    elif args.command == "check":
        return cmd_check(args)
    elif args.command == "index":
        return cmd_index(args)
    elif args.command == "hooks":
        return cmd_hooks(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
