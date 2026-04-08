"""
models.py — Typed Pydantic models for PhysicsEnv.
Defines Action, Observation, and State for the OpenEnv spec.
"""

from __future__ import annotations
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Action
# ---------------------------------------------------------------------------

class PhysicsAction(BaseModel):
    """
    The action an agent takes: submit a numerical answer (with optional unit).
    """
    answer: float = Field(..., description="Numerical answer to the physics problem")
    unit: str = Field(default="", description="Unit of the answer (e.g. 'm/s', 'J', 'kg')")
    reasoning: str = Field(default="", description="Optional chain-of-thought reasoning")


# ---------------------------------------------------------------------------
# Observation
# ---------------------------------------------------------------------------

class PhysicsObservation(BaseModel):
    """
    What the agent observes after reset() or step().
    """
    problem_id: str = Field(..., description="Unique ID of the current problem")
    domain: str = Field(..., description="Physics domain (e.g. 'classical_mechanics')")
    difficulty: str = Field(..., description="Difficulty level: easy | medium | hard")
    question: str = Field(..., description="Full text of the physics problem")
    given_variables: Dict[str, Any] = Field(default_factory=dict,
                                             description="Named variables provided in the problem")
    expected_unit: str = Field(default="", description="Expected unit of the answer")
    hint: str = Field(default="", description="Optional hint (empty on first step)")
    feedback: str = Field(default="", description="Feedback on the last action (empty on reset)")
    done: bool = Field(default=False, description="Whether the episode is finished")
    reward: float = Field(default=0.0, description="Reward from the last step (0 on reset)")


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

class PhysicsState(BaseModel):
    """
    Internal episode metadata exposed via GET /state.
    """
    episode_id: str = Field(default="", description="UUID of the current episode")
    task_name: str = Field(default="", description="Active task name")
    current_problem_index: int = Field(default=0, description="Index within the task problem list")
    total_problems: int = Field(default=0, description="Total problems in this episode")
    problems_solved: int = Field(default=0, description="Number of problems solved correctly")
    cumulative_reward: float = Field(default=0.0, description="Total reward accumulated so far")
    steps_taken: int = Field(default=0, description="Number of step() calls so far")
    done: bool = Field(default=False, description="Whether the episode is complete")
