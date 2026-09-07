from __future__ import annotations

HOTPOTQA_EXAMPLES = """Question: What is the elevation range for the area that the eastern sector of the Colorado orogeny extends into?
Thought 1: I should find what area the eastern sector extends into first.
Action 1: Search[Colorado orogeny]
Observation 1: The Colorado orogeny was an episode of mountain building in Colorado and surrounding areas. The eastern sector of the orogeny extended into the High Plains.
Thought 2: Now I need the elevation range of the High Plains.
Action 2: Search[High Plains]
Observation 2: High Plains refers to one of the two distinct land regions of the Great Plains. The High Plains rise in elevation from around 1,800 to 7,000 ft.
Thought 3: I have the elevation range.
Action 3: Finish[approximately 1,800 to 7,000 ft]

Question: Musician and satirist Allie Goertz wrote a song about the "The Simpsons" character Milhouse, who was named after who?
Thought 1: I need to search Milhouse and check who he was named after.
Action 1: Search[Milhouse Van Houten]
Observation 1: Milhouse Mussolini Van Houten is a recurring character in The Simpsons. Milhouse was named after U.S. president Richard Nixon.
Thought 2: The answer is Richard Nixon.
Action 2: Finish[Richard Nixon]"""


FEVER_EXAMPLES = """Claim: Stranger Things is set in Bloomington, Indiana.
Thought 1: I should verify the setting of Stranger Things.
Action 1: Search[Stranger Things]
Observation 1: Stranger Things is set primarily in the fictional town of Hawkins, Indiana.
Thought 2: The claim says Bloomington, but evidence says Hawkins.
Action 2: Finish[REFUTES]

Claim: "Beautiful" by Christina Aguilera reached number two on the Billboard Hot 100.
Thought 1: I need to check chart performance for this song.
Action 1: Search[Beautiful Christina Aguilera song]
Observation 1: "Beautiful" is a song by Christina Aguilera. The song reached number two on the Billboard Hot 100.
Thought 2: The evidence directly supports the claim.
Action 2: Finish[SUPPORTS]"""


HOTPOTQA_TEMPLATE = """Solve the question with interleaving Thought, Action, Observation steps.

Actions allowed:
1. Search[entity]
2. Lookup[keyword]
3. Finish[answer]

Examples:
{examples}

Question: {question}
{trajectory}
Thought {next_step}:"""


FEVER_TEMPLATE = """Classify the claim as SUPPORTS, REFUTES, or NOT ENOUGH INFO using Thought, Action, Observation steps.

Actions allowed:
1. Search[entity]
2. Lookup[keyword]
3. Finish[label]

Examples:
{examples}

Claim: {question}
{trajectory}
Thought {next_step}:"""


def build_prompt(task: str, question: str, trajectory: str, next_step: int) -> str:
    trajectory_block = trajectory + "\n" if trajectory else ""

    if task == "hotpotqa":
        return HOTPOTQA_TEMPLATE.format(
            examples=HOTPOTQA_EXAMPLES,
            question=question,
            trajectory=trajectory_block,
            next_step=next_step,
        )

    if task == "fever":
        return FEVER_TEMPLATE.format(
            examples=FEVER_EXAMPLES,
            question=question,
            trajectory=trajectory_block,
            next_step=next_step,
        )

    raise ValueError("task must be 'hotpotqa' or 'fever'")
