"""
app.py — FastAPI server for PhysicsEnv.
Exposes POST /reset, POST /step, GET /state, GET /health, GET /tasks
"""

from __future__ import annotations
import sys
import os
import uvicorn  # Added for deployment entry point

# Make sure parent directory (where models.py, problems.py, grader.py live) is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

from server.physics_environment import PhysicsEnvironment
from problems import TASK_LIST

app = FastAPI(
    title="PhysicsEnv",
    description="OpenEnv RL environment for multi-domain physics problem solving",
    version="1.0.0",
)

# Single shared environment instance (concurrent sessions disabled)
_env = PhysicsEnvironment()


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------

class ResetRequest(BaseModel):
    task_name: Optional[str] = None


class StepRequest(BaseModel):
    answer: float
    unit: str = ""
    reasoning: str = ""


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/")
def read_root():
    # Updated to direct users to your Swagger UI
    return {"message": "Welcome to PhysicsEnv! Go to /docs for the API interface."}

@app.get("/health")
def health():
    return {"status": "ok", "environment": "physics_env"}


@app.get("/tasks")
def list_tasks():
    return {"tasks": TASK_LIST}


@app.post("/reset")
def reset(req: ResetRequest = ResetRequest()):
    obs = _env.reset(task_name=req.task_name)
    return JSONResponse(content={"observation": obs, "reward": 0.0, "done": False})


@app.post("/step")
def step(req: StepRequest):
    result = _env.step({"answer": req.answer, "unit": req.unit, "reasoning": req.reasoning})
    return JSONResponse(content=result)


@app.get("/state")
def state():
    return JSONResponse(content=_env.state())


# ---------------------------------------------------------------------------
# Deployment Entry Point
# ---------------------------------------------------------------------------
def main():
    """Entry point for the deployment server."""
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
