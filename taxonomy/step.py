"""
Lightweight step/pipeline primitives for local data processing workflows.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(kw_only=True)
class Step:
    name: str = ""
    enabled: bool = True

    @property
    def step_name(self) -> str:
        return self.name or self.__class__.__name__

    def run(self) -> dict[str, Any]:
        """Execute the step and return a result mapping."""
        raise NotImplementedError


@dataclass
class Pipeline:
    steps: list[Step]
    name: str = "pipeline"

    def run(self) -> list[dict[str, Any]]:
        if not self.steps:
            raise ValueError(f"Pipeline '{self.name}' has no steps.")

        total_steps = len(self.steps)
        results: list[dict[str, Any]] = []
        print(f"=== Pipeline Start ({self.name}, steps: {total_steps}) ===")
        for index, step in enumerate(self.steps, start=1):
            if not step.enabled:
                print(f"[{index}/{total_steps}] Skip: {step.step_name}")
                continue
            print(f"\n[{index}/{total_steps}] Run: {step.step_name}")
            result = step.run()
            if not isinstance(result, dict):
                result = {"result": result}
            results.append({"name": step.step_name, "index": index, "result": result})
            if result:
                print(f"[{step.step_name}] result: {result}")
        print(f"\n=== Pipeline Complete ({self.name}) ===")
        return results
