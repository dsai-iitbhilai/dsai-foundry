from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL_ID = "Sid1409/disaster-tweet-classifier"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)
model.eval()

def predict(text: str) -> dict:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
    with torch.no_grad():
        logits = model(**inputs).logits
    pred = torch.argmax(logits, dim=1).item()
    prob = torch.softmax(logits, dim=1)[0][pred].item()
    label = {0: "not_disaster", 1: "disaster"}[pred]
    return {"label": label, "confidence": round(prob, 4)}

if __name__ == "__main__":
    samples = [
        "Wildfire spreading across California hills, thousands evacuated",
        "I'm on fire today at the gym!",
    ]
    for s in samples:
        print(f"{s!r} → {predict(s)}")