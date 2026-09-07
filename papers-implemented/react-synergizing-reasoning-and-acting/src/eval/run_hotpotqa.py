import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from eval.metrics import exact_match, f1_score
from react_agent.agent import ReactAgent
from react_agent.llm import LLMClient


HOTPOTQA_SAMPLES = [
    {
        "question": "What is the elevation range for the area that the eastern sector of the Colorado orogeny extends into?",
        "answer": "approximately 1,800 to 7,000 ft",
    },
    {
        "question": "Musician and satirist Allie Goertz wrote a song about the 'The Simpsons' character Milhouse, who was named after who?",
        "answer": "Richard Nixon",
    },
    {
        "question": "Which documentary is about Finnish rock groups, 'The Saimaa Gesture' or 'Global Metal'?",
        "answer": "The Saimaa Gesture",
    },
    {
        "question": "What is the capital of the country where the Cheli La pass is located?",
        "answer": "Thimphu",
    },
    {
        "question": "What nationality is the creator of the TV series 'Lost'?",
        "answer": "American",
    },
]


def run_evaluation(n: int = 5, verbose: bool = False):
    llm = LLMClient()
    samples = HOTPOTQA_SAMPLES[:n]

    total_em = 0.0
    total_f1 = 0.0
    results = []

    print(f"Running HotpotQA subset with {len(samples)} samples")
    for i, sample in enumerate(samples, start=1):
        question = sample["question"]
        gold = sample["answer"]

        agent = ReactAgent(task="hotpotqa", llm=llm)
        pred, trace = agent.run(question)

        em = exact_match(pred, gold)
        f1 = f1_score(pred, gold)
        total_em += em
        total_f1 += f1

        results.append({
            "question": question,
            "gold": gold,
            "predicted": pred,
            "em": em,
            "f1": f1,
            "steps": len(trace),
        })

        print(f"[{i}] EM={em:.0f} F1={f1:.2f} | pred={pred}")
        if verbose:
            agent.print_trace()

        time.sleep(1)

    print("\nSummary")
    print(f"EM: {total_em / len(samples):.2%}")
    print(f"F1: {total_f1 / len(samples):.2%}")
    print(f"Tokens: {llm.total_tokens_used}")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    run_evaluation(n=args.n, verbose=args.verbose)
