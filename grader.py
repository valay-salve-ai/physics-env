"""
grader.py — Grading logic for PhysicsEnv.

Reward schema:
  1.0   — Answer within tolerance AND unit matches (if expected)
  0.7   — Answer within tolerance, unit missing or wrong
  0.3   — Answer within 10× tolerance (partial credit: right ballpark)
  0.1   — Correct order of magnitude only
  0.0   — Wrong
"""

from __future__ import annotations
import math
from typing import Tuple


def _orders_match(answer: float, expected: float) -> bool:
    """Return True if answer and expected are within 1 order of magnitude."""
    if expected == 0:
        return abs(answer) < 1e-10
    ratio = abs(answer / expected)
    return 0.1 <= ratio <= 10.0


def _unit_ok(submitted: str, expected: str) -> bool:
    """
    Loose unit check — lower-case, strip spaces.
    Empty expected_unit means unit is dimensionless or not checked.
    """
    if not expected:
        return True
    return submitted.strip().lower() == expected.strip().lower()


def grade(
    answer: float,
    unit: str,
    expected_answer: float,
    expected_unit: str,
    tolerance: float,
) -> Tuple[float, str]:
    """
    Returns (reward: float, feedback: str).
    reward is in [0.0, 1.0].
    """
    if expected_answer == 0:
        within_tol = abs(answer) <= 1e-10
        within_10x = abs(answer) <= 1e-9
    else:
        rel_error = abs(answer - expected_answer) / abs(expected_answer)
        within_tol = rel_error <= tolerance
        within_10x = rel_error <= 10 * tolerance

    unit_correct = _unit_ok(unit, expected_unit)
    order_ok = _orders_match(answer, expected_answer)

    if within_tol and unit_correct:
        reward = 1.0
        feedback = (
            f"✅ Correct! Answer {answer} {unit} matches expected "
            f"{expected_answer} {expected_unit} within {tolerance*100:.0f}% tolerance."
        )
    elif within_tol and not unit_correct:
        reward = 0.7
        feedback = (
            f"⚠️ Numerically correct ({answer}) but unit '{unit}' doesn't match "
            f"expected '{expected_unit}'. Partial credit awarded."
        )
    elif within_10x:
        reward = 0.3
        feedback = (
            f"🔶 Close but not within tolerance. Your answer: {answer} {unit}, "
            f"expected: {expected_answer} {expected_unit}. "
            f"You're in the right ballpark — check your arithmetic."
        )
    elif order_ok:
        reward = 0.1
        feedback = (
            f"🔸 Correct order of magnitude but off. Your answer: {answer} {unit}, "
            f"expected: {expected_answer} {expected_unit}. "
            f"Check your formula and constants."
        )
    else:
        reward = 0.0
        feedback = (
            f"❌ Incorrect. Your answer: {answer} {unit}, "
            f"expected: {expected_answer} {expected_unit}. "
            f"Review the relevant physics principles."
        )

    return reward, feedback
