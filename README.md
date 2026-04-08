# PhysicsEnv 🔬

**An OpenEnv RL environment for solving multi-domain physics problems.**

An LLM agent receives physics problems spanning Classical Mechanics, Newtonian Mechanics, Quantum Mechanics, Special Relativity, Electromagnetism, and Thermodynamics — and must return the correct numerical answer with units.

---

## 🧠 Environment Description

| Property | Value |
|---|---|
| Framework | OpenEnv |
| Action Space | `{answer: float, unit: string, reasoning: string}` |
| Observation Space | `{problem_id, domain, difficulty, question, given_variables, expected_unit, hint, feedback, done, reward}` |
| Reward Range | `[0.0, 1.0]` |
| Tasks | 3 (easy, medium, hard) |
| Total Problems | 15 (5 per task) |

---

## 📚 Tasks

### 1. `classical_mechanics_easy` (Easy)
Classic kinematics and Newton's laws:
- Uniform acceleration (v = v₀ + at)
- Projectile motion
- Newton's 2nd Law (F = ma)
- Energy conservation
- Hooke's Law

### 2. `thermodynamics_medium` (Medium)
Thermodynamics and Electromagnetism:
- Combined gas law
- Calorimetry (Q = mcΔT)
- Coulomb's Law
- Ohm's Law / Power
- Carnot efficiency

### 3. `quantum_relativity_hard` (Hard)
Quantum mechanics and Special Relativity:
- de Broglie wavelength
- Photon energy (E = hf)
- Time dilation
- Mass-energy equivalence (E = mc²)
- Particle-in-a-box ground state energy

---

## 🏆 Reward Schema

| Condition | Reward |
|---|---|
| Correct answer + correct unit | **1.0** |
| Correct answer + wrong/missing unit | **0.7** |
| Within 10× tolerance (right ballpark) | **0.3** |
| Correct order of magnitude only | **0.1** |
| Wrong | **0.0** |

---

## 🚀 Quick Start

### 1. Local setup

```bash
pip install -r requirements.txt
```

### 2. Run the server

```bash
uvicorn server.app:app --host 0.0.0.0 --port 7860
```

### 3. Test manually

```bash
# Health check
curl http://localhost:7860/health

# List tasks
curl http://localhost:7860/tasks

# Reset (start episode)
curl -X POST http://localhost:7860/reset \
  -H "Content-Type: application/json" \
  -d '{"task_name": "classical_mechanics_easy"}'

# Step (submit answer)
curl -X POST http://localhost:7860/step \
  -H "Content-Type: application/json" \
  -d '{"answer": 15.0, "unit": "m/s"}'

# State
curl http://localhost:7860/state
```

### 4. Run inference baseline

```bash
export API_BASE_URL="https://api.openai.com/v1"
export MODEL_NAME="gpt-4o-mini"
export HF_TOKEN="your-api-key"
export ENV_BASE_URL="http://localhost:7860"

python inference.py
```

---

## 🐳 Docker

```bash
# Build
docker build -t physics-env:latest .

# Run
docker run -p 7860:7860 physics-env:latest
```

---

## 🔌 API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Health check |
| `/tasks` | GET | List available tasks |
| `/reset` | POST | Start new episode |
| `/step` | POST | Submit answer, get reward |
| `/state` | GET | Episode metadata |

### Reset Request
```json
{"task_name": "classical_mechanics_easy"}
```

### Step Request
```json
{
  "answer": 15.0,
  "unit": "m/s",
  "reasoning": "v = v0 + at = 0 + 3.0 * 5.0 = 15.0"
}
```

### Step Response
```json
{
  "observation": {
    "problem_id": "cm_easy_002",
    "domain": "classical_mechanics",
    "difficulty": "easy",
    "question": "A ball is thrown horizontally...",
    "given_variables": {"h": "20 m", "g": "9.8 m/s²"},
    "expected_unit": "s",
    "hint": "Use h = 0.5 * g * t²",
    "feedback": "✅ Correct! ...",
    "done": false,
    "reward": 1.0
  },
  "reward": 1.0,
  "done": false,
  "info": {"expected_answer": 15.0, "expected_unit": "m/s"}
}
```

---

## 📁 Project Structure

```
physics_env/
├── __init__.py
├── models.py               # Pydantic Action/Observation/State models
├── problems.py             # Physics problem bank (15 problems, 3 difficulties)
├── grader.py               # Reward/grading logic
├── openenv.yaml            # OpenEnv manifest
├── pyproject.toml          # Package config
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container definition
├── inference.py            # Baseline LLM inference script (root-level, required)
└── server/
    ├── __init__.py
    ├── app.py              # FastAPI server
    └── physics_environment.py  # Core environment logic
```

---

## ⚙️ Environment Variables

| Variable | Description | Example |
|---|---|---|
| `API_BASE_URL` | LLM API endpoint | `https://api.openai.com/v1` |
| `MODEL_NAME` | Model identifier | `gpt-4o-mini` |
| `HF_TOKEN` | Hugging Face / API key | `hf_...` |
| `ENV_BASE_URL` | Running env URL | `http://localhost:7860` |

---

## 📝 Inference Log Format

```json
{"type": "[START]", "task": "classical_mechanics_easy", "total_problems": 5, "model": "gpt-4o-mini", "timestamp": 1234567890}
{"type": "[STEP]", "step": 1, "problem_id": "cm_easy_001", "domain": "classical_mechanics", "difficulty": "easy", "answer": 15.0, "unit": "m/s", "reward": 1.0, "done": false, "feedback": "✅ Correct!", "timestamp": 1234567891}
{"type": "[END]", "task": "classical_mechanics_easy", "total_steps": 5, "problems_solved": 4, "total_problems": 5, "cumulative_reward": 4.2, "mean_reward": 0.84, "timestamp": 1234567892}
```

---

## 🏗️ Deploying to Hugging Face Spaces

1. Create a new Space on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Set SDK to **Docker**
3. Push this repository to the Space
4. Add secrets: `API_BASE_URL`, `MODEL_NAME`, `HF_TOKEN`
5. The Space will auto-build and deploy

---

## 📖 Physics Domains Covered

- **Classical Mechanics** — kinematics, dynamics, energy, simple harmonic motion
- **Newtonian Mechanics** — Newton's laws, momentum, forces
- **Thermodynamics** — ideal gas law, heat, Carnot cycle
- **Electromagnetism** — Coulomb's law, circuits, Ohm's law
- **Quantum Mechanics** — de Broglie wavelength, photon energy, particle in a box
- **Special Relativity** — time dilation, mass-energy equivalence
