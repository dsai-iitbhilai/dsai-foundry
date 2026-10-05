# 🧠 Trained Models

This folder contains models trained by DSAI club members. Each entry is a self-contained directory with code, results, and documentation.

## How to Submit

1. Run `python foundry.py new --category trained-models` (or copy the `_template/` folder)
2. Fill in the code in `src/`, results in `results/`, and complete `README.md`
3. Host your model weights externally on [Hugging Face Hub](https://huggingface.co/) and link them
4. Run `python foundry.py check` to validate locally, then open a pull request — see [CONTRIBUTING.md](../CONTRIBUTING.md)

## Template

→ [`_template/`](_template/) — copy this folder to get started

## Entries

| Entry | Contributor | Description |
|-------|-------------|-------------|
| [Disaster Tweet Classifier (DistilBERT)](disaster-tweet-classifier/) | [@Siddhesh1420](https://github.com/Siddhesh1420) | Fine-tuned DistilBERT on 7.6k disaster tweets achieving 84% accuracy and F1, with SafeTensors weights hosted on HuggingFace. |
| *Your entry here* | — | [Submit yours →](../CONTRIBUTING.md) |
