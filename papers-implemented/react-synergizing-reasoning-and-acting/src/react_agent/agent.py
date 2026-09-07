import re

from .llm import LLMClient
from .prompts import build_prompt
from .tools import WikipediaEnv


class ReactAgent:
    """Minimal ReAct loop for learning the paper implementation."""

    def __init__(self, task: str = "hotpotqa", llm: LLMClient | None = None, max_steps: int = 7):
        if task not in {"hotpotqa", "fever"}:
            raise ValueError("task must be 'hotpotqa' or 'fever'")

        self.task = task
        self.llm = llm or LLMClient()
        self.max_steps = max_steps
        self.env = WikipediaEnv()
        self.trajectory: list[dict] = []

    def run(self, question: str) -> tuple[str, list[dict]]:
        self.trajectory = []
        self.env.reset()

        answer = "I could not finish within max steps."

        for step in range(1, self.max_steps + 1):
            prompt = build_prompt(
                task=self.task,
                question=question,
                trajectory=self._format_trajectory(),
                next_step=step,
            )

            response = self.llm.generate(
                prompt,
                stop=[f"\nObservation {step}:", "\nObservation:"],
            )
            thought, action, action_input = self._parse_response(response, step)

            if action.lower() == "finish":
                observation = action_input
                answer = action_input
            else:
                observation = self.env.step(action, action_input)

            self.trajectory.append(
                {
                    "step": step,
                    "thought": thought,
                    "action": action,
                    "action_input": action_input,
                    "observation": observation,
                }
            )

            if action.lower() == "finish":
                break

        return answer, self.trajectory

    def _parse_response(self, response: str, step: int) -> tuple[str, str, str]:
        thought_match = re.search(
            rf"Thought\s*{step}\s*:\s*(.*?)(?=Action\s*{step}\s*:|$)",
            response,
            re.IGNORECASE | re.DOTALL,
        )
        thought = thought_match.group(1).strip() if thought_match else response.strip()

        action_match = re.search(
            r"Action\s*\d*\s*:\s*(\w+)\s*\[(.*?)\]",
            response,
            re.IGNORECASE | re.DOTALL,
        )
        if not action_match:
            action_match = re.search(r"(\w+)\s*\[(.*?)\]", response, re.IGNORECASE | re.DOTALL)

        if action_match:
            action = action_match.group(1).strip()
            action_input = action_match.group(2).strip()
            return thought, action, action_input

        return thought, "Finish", "NOT ENOUGH INFO" if self.task == "fever" else thought

    def _format_trajectory(self) -> str:
        if not self.trajectory:
            return ""

        lines = []
        for item in self.trajectory:
            n = item["step"]
            lines.append(f"Thought {n}: {item['thought']}")
            lines.append(f"Action {n}: {item['action']}[{item['action_input']}]")
            lines.append(f"Observation {n}: {item['observation']}")
        return "\n".join(lines)

    def print_trace(self):
        for item in self.trajectory:
            n = item["step"]
            print(f"\nStep {n}")
            print(f"Thought {n}: {item['thought']}")
            print(f"Action {n}: {item['action']}[{item['action_input']}]")
            print(f"Observation {n}: {item['observation']}")
