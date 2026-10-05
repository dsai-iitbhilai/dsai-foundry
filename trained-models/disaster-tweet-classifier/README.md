# Disaster Tweet Classifier (DistilBERT)

Fine-tuned DistilBERT on 7.6k disaster tweets achieving 84% accuracy and F1,
with SafeTensors weights hosted on HuggingFace.

## Model

| Detail | Value |
|---|---|
| Base model | `distilbert-base-uncased` |
| Task | Binary text classification |
| Dataset | NLP with Disaster Tweets (Kaggle) |
| Train samples | ~7,600 |
| Accuracy | 84% |
| F1 Score | 84% |
| Weights | [Sid1409/disaster-tweet-classifier](https://huggingface.co/Sid1409/disaster-tweet-classifier) |

## Setup

```bash
pip install -r requirements.txt
```

## Run Inference

```bash
python src/inference.py
```

## How It Works

DistilBERT tokenizes the input tweet and passes it through a fine-tuned
classification head that outputs a binary label: `disaster` or `not_disaster`.