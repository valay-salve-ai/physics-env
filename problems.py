"""
problems.py — Physics problem bank.
Contains problems across 6 domains, 3 difficulty levels.
Each problem specifies the expected numerical answer and tolerance.
"""

from typing import List, Dict, Any

# Structure: each problem is a dict with keys:
#   id, domain, difficulty, question, given_variables,
#   expected_answer (float), tolerance (fraction, e.g. 0.02 = 2%),
#   expected_unit, hint

PROBLEMS: List[Dict[str, Any]] = [

    # =========================================================
    # EASY — Classical / Newtonian Mechanics
    # =========================================================
    {
        "id": "cm_easy_001",
        "domain": "classical_mechanics",
        "difficulty": "easy",
        "question": (
            "A car starts from rest and accelerates uniformly at 3.0 m/s². "
            "What is its velocity after 5.0 seconds?"
        ),
        "given_variables": {"a": "3.0 m/s²", "t": "5.0 s", "v0": "0 m/s"},
        "expected_answer": 15.0,
        "tolerance": 0.05,
        "expected_unit": "m/s",
        "hint": "Use v = v0 + a*t",
    },
    {
        "id": "cm_easy_002",
        "domain": "classical_mechanics",
        "difficulty": "easy",
        "question": (
            "A ball is thrown horizontally from a cliff 20 m high. "
            "How long does it take to hit the ground? (g = 9.8 m/s²)"
        ),
        "given_variables": {"h": "20 m", "g": "9.8 m/s²"},
        "expected_answer": 2.0203,
        "tolerance": 0.05,
        "expected_unit": "s",
        "hint": "Use h = 0.5 * g * t²",
    },
    {
        "id": "cm_easy_003",
        "domain": "classical_mechanics",
        "difficulty": "easy",
        "question": (
            "A 5 kg box is pushed with a net force of 20 N. "
            "What is its acceleration?"
        ),
        "given_variables": {"m": "5 kg", "F": "20 N"},
        "expected_answer": 4.0,
        "tolerance": 0.05,
        "expected_unit": "m/s²",
        "hint": "Newton's second law: F = m*a",
    },
    {
        "id": "cm_easy_004",
        "domain": "classical_mechanics",
        "difficulty": "easy",
        "question": (
            "A 10 kg object is dropped from rest. "
            "What is its kinetic energy after falling 5 m? (g = 9.8 m/s²)"
        ),
        "given_variables": {"m": "10 kg", "h": "5 m", "g": "9.8 m/s²"},
        "expected_answer": 490.0,
        "tolerance": 0.05,
        "expected_unit": "J",
        "hint": "KE gained = mgh (conservation of energy)",
    },
    {
        "id": "cm_easy_005",
        "domain": "classical_mechanics",
        "difficulty": "easy",
        "question": (
            "A spring has a spring constant k = 200 N/m. "
            "How much force is needed to compress it by 0.05 m?"
        ),
        "given_variables": {"k": "200 N/m", "x": "0.05 m"},
        "expected_answer": 10.0,
        "tolerance": 0.05,
        "expected_unit": "N",
        "hint": "Hooke's Law: F = k*x",
    },

    # =========================================================
    # MEDIUM — Thermodynamics & Electromagnetism
    # =========================================================
    {
        "id": "thermo_med_001",
        "domain": "thermodynamics",
        "difficulty": "medium",
        "question": (
            "An ideal gas occupies 2.0 L at 300 K and 1.0 atm. "
            "What volume does it occupy at 600 K and 2.0 atm?"
        ),
        "given_variables": {
            "V1": "2.0 L", "T1": "300 K", "P1": "1.0 atm",
            "T2": "600 K", "P2": "2.0 atm"
        },
        "expected_answer": 2.0,
        "tolerance": 0.05,
        "expected_unit": "L",
        "hint": "Use combined gas law: P1V1/T1 = P2V2/T2",
    },
    {
        "id": "thermo_med_002",
        "domain": "thermodynamics",
        "difficulty": "medium",
        "question": (
            "How much heat is required to raise the temperature of 2.0 kg of water "
            "from 20°C to 100°C? (specific heat of water = 4186 J/(kg·K))"
        ),
        "given_variables": {
            "m": "2.0 kg", "c": "4186 J/(kg·K)",
            "T1": "20°C", "T2": "100°C"
        },
        "expected_answer": 669760.0,
        "tolerance": 0.05,
        "expected_unit": "J",
        "hint": "Q = m * c * ΔT",
    },
    {
        "id": "em_med_001",
        "domain": "electromagnetism",
        "difficulty": "medium",
        "question": (
            "Two point charges of +3 μC and +3 μC are placed 0.1 m apart. "
            "What is the electrostatic force between them? "
            "(k = 8.99 × 10⁹ N·m²/C²)"
        ),
        "given_variables": {
            "q1": "3e-6 C", "q2": "3e-6 C",
            "r": "0.1 m", "k": "8.99e9 N·m²/C²"
        },
        "expected_answer": 8.091,
        "tolerance": 0.05,
        "expected_unit": "N",
        "hint": "Coulomb's law: F = k*q1*q2/r²",
    },
    {
        "id": "em_med_002",
        "domain": "electromagnetism",
        "difficulty": "medium",
        "question": (
            "A resistor of 50 Ω is connected to a 12 V battery. "
            "What is the power dissipated by the resistor?"
        ),
        "given_variables": {"R": "50 Ω", "V": "12 V"},
        "expected_answer": 2.88,
        "tolerance": 0.05,
        "expected_unit": "W",
        "hint": "P = V²/R",
    },
    {
        "id": "thermo_med_003",
        "domain": "thermodynamics",
        "difficulty": "medium",
        "question": (
            "A Carnot engine operates between hot reservoir T_H = 500 K "
            "and cold reservoir T_C = 300 K. What is its efficiency?"
        ),
        "given_variables": {"T_H": "500 K", "T_C": "300 K"},
        "expected_answer": 0.40,
        "tolerance": 0.05,
        "expected_unit": "",
        "hint": "Carnot efficiency: η = 1 - T_C/T_H",
    },

    # =========================================================
    # HARD — Quantum Mechanics & Special Relativity
    # =========================================================
    {
        "id": "qm_hard_001",
        "domain": "quantum_mechanics",
        "difficulty": "hard",
        "question": (
            "Calculate the de Broglie wavelength of an electron moving at "
            "2.0 × 10⁶ m/s. "
            "(h = 6.626 × 10⁻³⁴ J·s, m_e = 9.109 × 10⁻³¹ kg)"
        ),
        "given_variables": {
            "v": "2.0e6 m/s",
            "h": "6.626e-34 J·s",
            "m_e": "9.109e-31 kg"
        },
        "expected_answer": 3.638e-10,
        "tolerance": 0.05,
        "expected_unit": "m",
        "hint": "λ = h / (m * v)",
    },
    {
        "id": "qm_hard_002",
        "domain": "quantum_mechanics",
        "difficulty": "hard",
        "question": (
            "What is the energy of a photon with wavelength 500 nm? "
            "(h = 6.626 × 10⁻³⁴ J·s, c = 3.0 × 10⁸ m/s)"
        ),
        "given_variables": {
            "λ": "500e-9 m",
            "h": "6.626e-34 J·s",
            "c": "3.0e8 m/s"
        },
        "expected_answer": 3.976e-19,
        "tolerance": 0.05,
        "expected_unit": "J",
        "hint": "E = h*c/λ",
    },
    {
        "id": "rel_hard_001",
        "domain": "special_relativity",
        "difficulty": "hard",
        "question": (
            "A spaceship travels at v = 0.8c relative to Earth. "
            "If 10 years pass on Earth, how many years pass on the spaceship? "
            "(c = speed of light)"
        ),
        "given_variables": {"v": "0.8c", "t_earth": "10 years"},
        "expected_answer": 6.0,
        "tolerance": 0.05,
        "expected_unit": "years",
        "hint": "Time dilation: t_proper = t * sqrt(1 - v²/c²)",
    },
    {
        "id": "rel_hard_002",
        "domain": "special_relativity",
        "difficulty": "hard",
        "question": (
            "What is the rest-mass energy of a proton? "
            "(m_p = 1.673 × 10⁻²⁷ kg, c = 3.0 × 10⁸ m/s)"
        ),
        "given_variables": {
            "m_p": "1.673e-27 kg",
            "c": "3.0e8 m/s"
        },
        "expected_answer": 1.5057e-10,
        "tolerance": 0.05,
        "expected_unit": "J",
        "hint": "E = m*c²",
    },
    {
        "id": "qm_hard_003",
        "domain": "quantum_mechanics",
        "difficulty": "hard",
        "question": (
            "An electron is confined to a 1D box of length L = 1.0 nm. "
            "What is the ground-state (n=1) energy? "
            "(h = 6.626 × 10⁻³⁴ J·s, m_e = 9.109 × 10⁻³¹ kg)"
        ),
        "given_variables": {
            "L": "1.0e-9 m", "n": "1",
            "h": "6.626e-34 J·s",
            "m_e": "9.109e-31 kg"
        },
        "expected_answer": 6.024e-20,
        "tolerance": 0.05,
        "expected_unit": "J",
        "hint": "E_n = n²h²/(8mL²)",
    },
]

# Group by difficulty for easy task lookup
TASK_PROBLEMS = {
    "classical_mechanics_easy": [p for p in PROBLEMS if p["difficulty"] == "easy"],
    "thermodynamics_medium":    [p for p in PROBLEMS if p["difficulty"] == "medium"],
    "quantum_relativity_hard":  [p for p in PROBLEMS if p["difficulty"] == "hard"],
}

TASK_LIST = list(TASK_PROBLEMS.keys())
