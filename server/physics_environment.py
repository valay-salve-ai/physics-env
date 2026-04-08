"""
physics_environment.py — PhysicsEnvironment server-side implementation.
Subclasses the OpenEnv Environment base class.
"""

from __future__ import annotations
import uuid
from typing import Optional

from models import PhysicsAction, PhysicsObservation, PhysicsState
from problems import TASK_PROBLEMS, TASK_LIST
from grader import grade


class PhysicsEnvironment:
    """
    OpenEnv-compatible environment for solving multi-domain physics problems.

    Episode flow:
      reset(task_name?) → observation of first problem
      step(action)      → graded observation, reward, done flag
      state()           → current PhysicsState metadata
    """

    def __init__(self) -> None:
        self._state = PhysicsState()
        self._problems: list = []
        self._current_idx: int = 0

    # ------------------------------------------------------------------
    # OpenEnv API
    # ------------------------------------------------------------------

    def reset(self, task_name: Optional[str] = None) -> dict:
        """Start a new episode. Returns first observation as dict."""
        if task_name is None or task_name not in TASK_PROBLEMS:
            task_name = TASK_LIST[0]

        problems = TASK_PROBLEMS[task_name]
        self._problems = problems
        self._current_idx = 0

        self._state = PhysicsState(
            episode_id=str(uuid.uuid4()),
            task_name=task_name,
            current_problem_index=0,
            total_problems=len(problems),
            problems_solved=0,
            cumulative_reward=0.0,
            steps_taken=0,
            done=False,
        )

        return self._make_observation(reward=0.0, feedback="", done=False).model_dump()

    def step(self, action: dict) -> dict:
        """
        Execute one action. Returns StepResult-like dict with keys:
          observation, reward, done, info
        """
        if self._state.done:
            obs = self._make_observation(
                reward=0.0,
                feedback="Episode already finished. Call reset() to start a new episode.",
                done=True,
            )
            return {"observation": obs.model_dump(), "reward": 0.0, "done": True, "info": {}}

        act = PhysicsAction(**action) if isinstance(action, dict) else action
        problem = self._problems[self._current_idx]

        reward, feedback = grade(
            answer=act.answer,
            unit=act.unit,
            expected_answer=problem["expected_answer"],
            expected_unit=problem["expected_unit"],
            tolerance=problem["tolerance"],
        )

        self._state.steps_taken += 1
        self._state.cumulative_reward += reward
        if reward >= 0.7:
            self._state.problems_solved += 1

        # Advance to next problem
        self._current_idx += 1
        done = self._current_idx >= len(self._problems)
        self._state.current_problem_index = self._current_idx
        self._state.done = done

        obs = self._make_observation(reward=reward, feedback=feedback, done=done)

        return {
            "observation": obs.model_dump(),
            "reward": reward,
            "done": done,
            "info": {
                "expected_answer": problem["expected_answer"],
                "expected_unit": problem["expected_unit"],
            },
        }

    def state(self) -> dict:
        """Return current episode state metadata."""
        return self._state.model_dump()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _make_observation(
        self, reward: float, feedback: str, done: bool
    ) -> PhysicsObservation:
        if done or self._current_idx >= len(self._problems):
            # Terminal observation
            return PhysicsObservation(
                problem_id="DONE",
                domain="",
                difficulty=self._state.task_name,
                question=(
                    f"Episode complete! You solved "
                    f"{self._state.problems_solved}/{self._state.total_problems} problems "
                    f"with total reward {self._state.cumulative_reward:.2f}."
                ),
                given_variables={},
                expected_unit="",
                hint="",
                feedback=feedback,
                done=True,
                reward=reward,
            )

        problem = self._problems[self._current_idx]
        return PhysicsObservation(
            problem_id=problem["id"],
            domain=problem["domain"],
            difficulty=problem["difficulty"],
            question=problem["question"],
            given_variables=problem["given_variables"],
            expected_unit=problem["expected_unit"],
            hint=problem.get("hint", ""),
            feedback=feedback,
            done=False,
            reward=reward,
        )
