# Contributing to DSAI Foundry

Thank you for contributing! This guide covers everything you need to submit your work to the DSAI Foundry showcase using our automated developer tooling.

---

## Table of Contents

- [What Can I Submit?](#what-can-i-submit)
- [Submission Tiers](#submission-tiers)
- [Quickstart: 4-Step Contribution Workflow](#quickstart-4-step-contribution-workflow)
- [Developer Tooling (`foundry.py`)](#developer-tooling-foundrypy)
- [Folder Naming Convention](#folder-naming-convention)
- [Handling Large Files (< 10 MB Rule)](#handling-large-files--10-mb-rule)
- [Code Quality & Reproducibility](#code-quality--reproducibility)
- [PR Review & Automated CI Process](#pr-review--automated-ci-process)
- [Getting Help](#getting-help)

---

## What Can I Submit?

| Category | Folder | What Goes In It |
|----------|--------|-----------------|
| **Trained Models** | `trained-models/` | A model you trained — training scripts, metrics, reproducibility instructions, link to hosted weights |
| **Paper Implementations** | `papers-implemented/` | A from-scratch or adapted implementation of a published research paper, with reproduced results |
| **Projects** | `projects/` | A complete applied project — end-to-end data pipelines, full-stack ML apps, demos, or tools |

---

## Submission Tiers

We support three flexible submission tiers to accommodate different types of member work:

### 1. Full In-Repo Implementation (Tier A — Default)
- **Best for:** Standard models, paper reproductions, or scripts developed directly for DSAI Foundry.
- **Contents:** `src/`, `notebooks/`, `results/`, `requirements.txt`, `README.md`, `entry.json`.
- **Created via:** `python foundry.py new --tier full`

### 2. Notebook-First Submission (Tier B)
- **Best for:** Exploratory data analysis, Kaggle competition writeups, or single-file tutorial notebooks.
- **Contents:** `notebooks/demo.ipynb`, `results/`, `requirements.txt`, `README.md`, `entry.json`.
- **Created via:** `python foundry.py new --tier notebook`

### 3. Showcase / Linked Project (Tier C)
- **Best for:** Existing large repositories (e.g. multi-service web apps, mobile apps, or full systems) where you want to feature your work without copying thousands of external files.
- **Contents:** `README.md` (with system architecture, demo GIF/screenshots, results, and prominent link back to your standalone repository), `results/`, `entry.json`.
- **Created via:** `python foundry.py new --tier showcase`

---

## Quickstart: 4-Step Contribution Workflow

### Step 0: One-Time Local Setup

Clone your fork and enable the automated pre-commit guardrail:

```bash
git clone https://github.com/<your-username>/dsai-foundry.git
cd dsai-foundry
python foundry.py hooks
```
> 💡 `python foundry.py hooks` configures Git to automatically check file sizes and syntax before every commit, saving you from accidental large-file or secret pushes!

---

### Step 1: Create a Branch & Scaffold Your Entry

Create a feature branch and let the CLI generate your project structure:

```bash
git checkout -b add/my-awesome-entry
python foundry.py new
```

The interactive wizard will ask for:
1. **Category:** `trained-models`, `papers-implemented`, or `projects`
2. **Slug:** `kebab-case` name (e.g. `resnet50-cifar10`)
3. **Title & Summary:** What you built
4. **Author & GitHub Handle:** For leaderboard credit
5. **Tags:** Relevant topics (e.g. `nlp`, `agents`, `vision`)

*Non-interactive flag example:*
```bash
python foundry.py new --category papers-implemented --slug lora-finetuning --title "LoRA Fine-Tuning" --author "Jane Doe" --github janedoe --tags "nlp,llm,peft"
```

---

### Step 2: Develop Your Submission

- Place your runnable code in `src/` (or notebook in `notebooks/`).
- Document key metrics and sample plots in `results/`.
- Edit `README.md` to explain architecture, deviations, and how to run.
- Pin your dependencies in `requirements.txt`.
- If your code requires API keys, document them in `.env.example`.

---

### Step 3: Run Pre-Flight Validation Locally

Before pushing, verify that your entry conforms to all repository standards:

```bash
python foundry.py check
```

This automatically validates:
- 📦 **File size check:** Guarantees no file exceeds 10 MB.
- 🔒 **Secrets check:** Scans for unignored `.env` or leaked tokens.
- 🐍 **Syntax check:** Compiles all Python files to prevent syntax bugs.
- 📝 **Placeholder check:** Flags any template placeholders left unedited.

---

### Step 4: Commit & Open a Pull Request

```bash
git add .
git commit -m "feat(category): add <entry-slug>"
git push origin add/<entry-slug>
```

Open a PR against `main`.

> [!NOTE]
> **No manual edits to root `README.md` or `LEADERBOARD.md` are required!**  
> To prevent merge conflicts between concurrent PRs, directory tables and contributor rankings are automatically regenerated from `entry.json` upon merge.

---

## Developer Tooling (`foundry.py`)

`foundry.py` is our zero-dependency CLI located at the repository root:

| Command | Usage | Description |
|---|---|---|
| `foundry new` | `python foundry.py new` | Scaffolds an entry and pre-fills README placeholders. |
| `foundry check` | `python foundry.py check [path]` | Pre-flight validation for sizes, syntax, and secrets. |
| `foundry check --staged` | `python foundry.py check --staged` | Validates only currently staged Git files. |
| `foundry index` | `python foundry.py index` | Regenerates directory tables and leaderboard rankings. |
| `foundry index --check` | `python foundry.py index --check` | Verifies index consistency (used in CI). |
| `foundry hooks` | `python foundry.py hooks` | Configures Git to use local `.githooks/` pre-commit guard. |

---

## Folder Naming Convention

- Use **kebab-case** (lowercase, hyphens only):
  - ✅ `trained-models/resnet50-cifar10/`
  - ✅ `papers-implemented/react-synergizing-reasoning-and-acting/`
  - ✅ `projects/movie-recommender/`
- Avoid spaces, underscores, or uppercase characters:
  - ❌ `trained-models/ResNet50_CIFAR10/`
  - ❌ `papers-implemented/My Paper/`

---

## Handling Large Files (< 10 MB Rule)

**🚫 Never commit files over 10 MB.** Git repositories bloat permanently when large binary files are committed.

### Where to Host External Assets

| Asset Type | Recommended Platform | How to Link |
|---|---|---|
| **Model Weights** | [Hugging Face Hub](https://huggingface.co/) | Link model repository in your README |
| **Datasets** | [Kaggle](https://www.kaggle.com/datasets) / [HF Datasets](https://huggingface.co/datasets) | Link in README + optional download script |
| **Large Binaries / Media** | [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github) | Attach to release (up to 2 GB/file) |

---

## Code Quality & Reproducibility

- ✅ Code runs end-to-end from a clean `pip install -r requirements.txt`.
- ✅ No hardcoded absolute machine paths (`C:\Users\...` or `/home/...`).
- ✅ All dependencies have pinned versions.
- ✅ Clear instructions in `README.md` on how to run inference and evaluation.
- ❌ No API keys, passwords, or personal credentials committed.

---

## PR Review & Automated CI Process

1. **Automated CI Validation:** On PR submission, GitHub Actions automatically executes `foundry check` and `foundry index --check`.
2. **Peer Review:** A club maintainer reviews the code, results, and documentation.
3. **Merge & Spotlight:** Once approved, your entry joins the showcase, and you are automatically credited on the [Leaderboard](LEADERBOARD.md)!

---

## Getting Help

- 💬 Open an [issue](https://github.com/dsai-iitbhilai/dsai-foundry/issues) with the `question` label.
- 📋 Look for issues tagged [`good-first-implementation`](https://github.com/dsai-iitbhilai/dsai-foundry/issues?q=label%3Agood-first-implementation).
- 🗣️ Connect with us on DSAI Club communication channels.

*Happy building! 🚀*
