# Contributing to DSAI Foundry

Thank you for contributing! This guide covers everything you need to submit your work to the DSAI Foundry showcase.

---

## Table of Contents

- [What Can I Submit?](#what-can-i-submit)
- [Step-by-Step Workflow](#step-by-step-workflow)
- [Folder Naming Convention](#folder-naming-convention)
- [Required README Sections](#required-readme-sections)
- [Handling Large Files](#handling-large-files)
- [Code Quality Expectations](#code-quality-expectations)
- [PR Review Process](#pr-review-process)
- [Getting Help](#getting-help)

---

## What Can I Submit?

| Category | Folder | What Goes In It |
|----------|--------|-----------------|
| **Trained Models** | `trained-models/` | A model you trained — code, metrics, reproducibility steps, link to weights |
| **Paper Implementations** | `papers-implemented/` | A from-scratch or adapted implementation of a published paper, with reproduced results |
| **Projects** | `projects/` | A complete applied project — could combine models, data pipelines, apps, etc. |

---

## Step-by-Step Workflow

### 1. Fork & Clone

```bash
# Fork this repo on GitHub, then:
git clone https://github.com/<your-username>/dsai-foundry.git
cd dsai-foundry
```

### 2. Create a Branch

```bash
git checkout -b add/<your-entry-name>
```

### 3. Copy the Template

```bash
# Pick your category and copy the template
cp -r trained-models/_template trained-models/your-entry-name
# or
cp -r papers-implemented/_template papers-implemented/your-entry-name
# or
cp -r projects/_template projects/your-entry-name
```

### 4. Do the Work

- Write your code in `src/`
- Add notebooks in `notebooks/` (optional)
- Save results (metrics, plots, tables) in `results/`
- **Fill in every section** of the template `README.md`
- Add all Python dependencies to `requirements.txt`

### 5. Add Your Entry to the Root README

Open the root [`README.md`](README.md) and add a row to the appropriate table in the **Directory** section.

### 6. Commit & Push

```bash
git add .
git commit -m "feat: add <your-entry-name> to <category>"
git push origin add/<your-entry-name>
```

### 7. Open a Pull Request

Open a PR against `main`. Fill in the PR template checklist completely.

---

## Folder Naming Convention

- Use **kebab-case** (lowercase, hyphens): `mnist-cnn-classifier`, `attention-is-all-you-need`, `sentiment-analysis-app`
- Be descriptive but concise
- **Do not** use spaces, underscores, or capital letters

```
✅ trained-models/resnet50-cifar10/
✅ papers-implemented/attention-is-all-you-need/
✅ projects/movie-recommender/

❌ trained-models/ResNet50_CIFAR10/
❌ papers-implemented/My Paper Implementation/
❌ projects/proj1/
```

---

## Required README Sections

Every entry **must** include these sections in its README (the templates have them pre-filled):

### All Categories
- **Title & Badges** — entry name, framework badge
- **Overview** — what it does, problem domain
- **How to Run** — step-by-step reproduction instructions
- **Results** — metrics, plots, or tables
- **Requirements** — point to `requirements.txt`
- **Contributors** — name(s) and GitHub handles

### Trained Models (additional)
- Architecture, dataset, training details, link to model weights

### Paper Implementations (additional)
- Paper reference (title, authors, venue, link), reproduced results vs. paper's numbers

### Projects (additional)
- Demo link / screenshots, system architecture, tech stack

---

## Handling Large Files

**🚫 Never commit files over 10 MB** — this includes model weights, datasets, checkpoints, and large binaries.

### Where to Host

| File Type | Recommended Host | How to Link |
|-----------|-----------------|-------------|
| **Model weights** | [Hugging Face Hub](https://huggingface.co/) | Add the HF model URL to your README |
| **Datasets** | [Kaggle Datasets](https://www.kaggle.com/datasets) or [HF Datasets](https://huggingface.co/datasets) | Link in README + optional download script |
| **Other large files** | [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github) | Attach to a release (up to 2 GB/file) |

### Download Script (Optional)

If your entry needs a dataset, consider adding a `download_data.sh` or `download_data.py` script:

```python
# download_data.py
"""Download the dataset required for this entry."""
import urllib.request
import os

DATA_URL = "https://example.com/dataset.zip"
DATA_DIR = "data/"

os.makedirs(DATA_DIR, exist_ok=True)
urllib.request.urlretrieve(DATA_URL, os.path.join(DATA_DIR, "dataset.zip"))
print("Dataset downloaded to data/dataset.zip")
```

---

## Code Quality Expectations

- ✅ Code **runs end-to-end** from a clean `pip install -r requirements.txt`
- ✅ **Reproducible** — someone else can clone and get the same results
- ✅ `requirements.txt` lists **all** dependencies with versions (use `pip freeze > requirements.txt`)
- ✅ Code is reasonably **clean and commented**
- ✅ No hardcoded absolute paths (use relative paths)
- ❌ No API keys, passwords, or secrets committed

---

## PR Review Process

1. **Automated checks** — the PR template checklist must be complete
2. **Peer review** — a club maintainer will review your submission for:
   - README completeness
   - Code quality and reproducibility
   - Correct folder structure and naming
   - No large files committed
3. **Feedback** — you may be asked to make changes. This is normal!
4. **Merge** — once approved, your entry joins the showcase 🎉

---

## Getting Help

- 💬 Open an [issue](https://github.com/dsai-iitbhilai/dsai-foundry/issues) with the `question` label
- 📋 Check out issues labeled [`good-first-implementation`](https://github.com/dsai-iitbhilai/dsai-foundry/issues?q=label%3Agood-first-implementation) for beginner-friendly ideas
- 🗣️ Reach out in the DSAI club's communication channels

---

*Happy building! 🚀*
