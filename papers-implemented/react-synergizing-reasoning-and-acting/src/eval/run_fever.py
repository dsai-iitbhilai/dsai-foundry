import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from eval.metrics import accuracy
from react_agent.agent import ReactAgent
from react_agent.llm import LLMClient


FEVER_SAMPLES = [
    {"claim": "Nikolaj Coster-Waldau worked with the Fox Broadcasting Company.", "label": "SUPPORTS"},
    {"claim": "Stranger Things is set in Bloomington, Indiana.", "label": "REFUTES"},
    {"claim": "The Godfather was directed by Francis Ford Coppola.", "label": "SUPPORTS"},
    {"claim": "The Amazon River flows through Africa.", "label": "REFUTES"},
    {"claim": "Linux was created by Linus Torvalds.", "label": "SUPPORTS"},
]


def run_evaluation(n: int = 5, verbose: bool = False):
    llm = LLMClient()
    samples = FEVER_SAMPLES[:n]

    correct = 0.0
    results = []

    print(f"Running FEVER subset with {len(samples)} samples")
    for i, sample in enumerate(samples, start=1):
        claim = sample["claim"]
        gold = sample["label"]

        agent = ReactAgent(task="fever", llm=llm)
        pred, trace = agent.run(claim)

        acc = accuracy(pred, gold)
        correct += acc

        results.append({
            "claim": claim,
            "gold": gold,
            "predicted": pred,
            "accuracy": acc,
            "steps": len(trace),
        })

        print(f"[{i}] acc={acc:.0f} | pred={pred}")
        if verbose:
            agent.print_trace()

        time.sleep(1)

    print("\nSummary")
    print(f"Accuracy: {correct / len(samples):.2%}")
    print(f"Tokens: {llm.total_tokens_used}")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    run_evaluation(n=args.n, verbose=args.verbose)
