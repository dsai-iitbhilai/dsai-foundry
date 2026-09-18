<div align="center">

# 🧠 DSAI Foundry

**The Data Science & AI Club's living archive of member work**

[![Contributors](https://img.shields.io/github/contributors/dsai-iitbhilai/dsai-foundry?style=flat-square&color=blue)](https://github.com/dsai-iitbhilai/dsai-foundry/graphs/contributors)
[![Last Commit](https://img.shields.io/github/last-commit/dsai-iitbhilai/dsai-foundry?style=flat-square&color=green)](https://github.com/dsai-iitbhilai/dsai-foundry/commits/main)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](https://github.com/dsai-iitbhilai/dsai-foundry/blob/main/CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](https://github.com/dsai-iitbhilai/dsai-foundry/blob/main/LICENSE)

*Trained models · Paper implementations · Complete projects — all in one place.*

</div>

---

## 📖 About

DSAI Foundry is the central showcase repository of the **Data Science & AI (DSAI) Club**, bringing together members' work in one organized and accessible space. It features **trained ML models, research paper implementations, experiments, and complete projects**, making it easier to explore, learn, and build upon the work of fellow members.

**Why contribute?**
- 🏅 **Public credit** — your name, PR history, and [leaderboard](LEADERBOARD.md) placement
- 📄 **Portfolio-ready** — link directly from your resume and LinkedIn
- 🤝 **Community learning** — others can study, reproduce, and build on your work

> **Lightweight by design.** This repo holds code, docs, results, and links. Heavy files (model weights, datasets) live on purpose-built external platforms and get linked from each entry.

---

## 📂 Directory

### Trained Models

| Entry | Contributor | Description |
|-------|-------------|-------------|
| *Your entry here* | — | [Submit yours →](CONTRIBUTING.md) |

### Paper Implementations

| Entry | Contributor | Paper | Description |
|-------|-------------|-------|-------------|
| [ReAct](papers-implemented/react-synergizing-reasoning-and-acting/) | [@vatsalyd](https://github.com/vatsalyd) | [Yao et al., ICLR 2023](https://arxiv.org/abs/2210.03629) | Synergizing reasoning and acting agent with Wikipedia tools, evaluated on HotpotQA & FEVER <br> `agents` `reasoning` `nlp` `llm` |
| *Your entry here* | — | — | [Submit yours →](CONTRIBUTING.md) |

### Projects

| Entry | Contributor | Description |
|-------|-------------|-------------|
| *Your entry here* | — | [Submit yours →](CONTRIBUTING.md) |

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/dsai-iitbhilai/dsai-foundry.git
cd dsai-foundry

# Browse a specific entry (e.g. ReAct paper implementation)
cd papers-implemented/react-synergizing-reasoning-and-acting

# Install its dependencies
pip install -r requirements.txt

# Follow the entry's README for how to run
```

---

## 🤝 How to Contribute

We welcome contributions from all club members! With our automated CLI tooling, contributing is fast and conflict-free:

1. **Scaffold your entry** — run `python foundry.py new` (or copy the category's `_template/`)
2. **Build your work** — add your code/notebooks, results, dependencies, and fill in `README.md`
3. **Validate locally** — run `python foundry.py check` to verify file sizes, syntax, and secrets
4. **Open a PR** — follow the checklist; directory tables and leaderboard are auto-indexed upon merge!

📘 **Full guide → [CONTRIBUTING.md](CONTRIBUTING.md)**

---

## 📦 Large Files Policy

GitHub limits file sizes, so heavy artifacts live elsewhere:

| Artifact | Where to Host | Why |
|----------|---------------|-----|
| **Model weights** | [Hugging Face Hub](https://huggingface.co/) | Free, built for ML models, gives you a shareable model page |
| **Datasets** | [Kaggle](https://www.kaggle.com/datasets) / [HF Datasets](https://huggingface.co/datasets) / source | Versioned, discoverable, handles large files |
| **Large binaries** | [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github) | Up to 2 GB per file, attached to the repo |

> **Rule of thumb:** if it's over 10 MB, it shouldn't be committed. Link it instead.

---

## 🏆 Recognition

We believe in celebrating contributions:

- **📊 [Leaderboard](LEADERBOARD.md)** — see who's contributed the most
- **⭐ Model/Paper of the Month** — featured spotlight in the leaderboard
- **🎖️ Badges** — earn milestone badges for your contributions

---

## 📜 License

This project is licensed under the [MIT License](LICENSE). Individual contributors retain copyright on their entries.
