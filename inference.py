import asyncio
import os
import textwrap
import json
import httpx
from typing import List, Optional

from openai import OpenAI

# ==============================================================================
# MANDATORY VARIABLES (Kept exactly as requested)
# ==============================================================================
# from my_env_v4 import MyEnvV4Action, MyEnvV4Env  <-- COMMENTED OUT (Placeholder only)
IMAGE_NAME = os.getenv("IMAGE_NAME") # If you are using docker image 
API_KEY = os.getenv("HF_TOKEN") or os.getenv("")

API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"

# I updated the fallbacks to point to your physics tasks so it doesn't try to load "echo"
TASK_NAME = os.getenv("MY_ENV_V4_TASK", "thermodynamics_medium")
BENCHMARK = os.getenv("MY_ENV_V4_BENCHMARK", "physics_env")

MAX_STEPS = 8
TEMPERATURE = 0.0 # Set to 0.0 for deterministic math answers
MAX_TOKENS = 150
SUCCESS_SCORE_THRESHOLD = 0.1  # normalized score in [0, 1]

_MAX_REWARD_PER_STEP = MAX_TOKENS * 0.1
MAX_TOTAL_REWARD = MAX_STEPS * _MAX_REWARD_PER_STEP
# ==============================================================================


LOCAL_URL = "http://localhost:7860"

SYSTEM_PROMPT = textwrap.dedent(
    """
    You are an expert physics solver. You must return ONLY a valid JSON object.
    Keys required:
    - "answer": A float/integer representing the numerical answer. Provide integers if possible.
    - "unit": A string representing the unit.
    - "reasoning": A brief string explaining your steps.
    """
).strip()


def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)


def build_user_prompt(step: int, obs: dict, last_reward: float, history: List[str]) -> str:
    history_block = "\n".join(history[-4:]) if history else "None"
    return textwrap.dedent(
        f"""
        Step: {step}
        Problem: {obs.get('question')}
        Given variables: {obs.get('given_variables')}
        Expected unit: {obs.get('expected_unit')}
        Last reward: {last_reward:.2f}
        Previous steps:
        {history_block}
        Solve the problem and send your JSON solution.
        """
    ).strip()


def get_model_message(client: OpenAI, step: int, obs: dict, last_reward: float, history: List[str]) -> dict:
    user_prompt = build_user_prompt(step, obs, last_reward, history)
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            response_format={"type": "json_object"}
        )
        text = (completion.choices[0].message.content or "").strip()
        return json.loads(text)
    except Exception as exc:
        print(f"[DEBUG] Model request failed: {exc}", flush=True)
        return {"answer": 0.0, "unit": "", "reasoning": f"Error: {exc}"}


async def wait_for_server():
    """Wait for the FastAPI server to be healthy before starting inference."""
    async with httpx.AsyncClient() as client:
        for _ in range(15):
            try:
                resp = await client.get(f"{LOCAL_URL}/health")
                if resp.status_code == 200:
                    return True
            except httpx.RequestError:
                await asyncio.sleep(1)
    return False


async def main() -> None:
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    if not await wait_for_server():
        print("[DEBUG] FastAPI server failed to start.", flush=True)
        log_end(success=False, steps=0, score=0.0, rewards=[])
        return

    history: List[str] = []
    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    try:
        async with httpx.AsyncClient(timeout=30.0) as http_client:
            # 1. Reset Environment
            reset_resp = await http_client.post(f"{LOCAL_URL}/reset", json={"task_name": TASK_NAME})
            result = reset_resp.json()
            
            obs = result["observation"]
            last_reward = 0.0
            done = result["done"]

            # 2. Step Loop
            for step in range(1, MAX_STEPS + 1):
                if done:
                    break

                # Get action from LLM
                action_dict = get_model_message(client, step, obs, last_reward, history)
                
                # Compress action to single line for logging requirements
                action_str = json.dumps(action_dict).replace('\n', ' ')

                # Execute step against FastAPI
                step_resp = await http_client.post(f"{LOCAL_URL}/step", json=action_dict)
                result = step_resp.json()
                
                obs = result["observation"]
                reward = result.get("reward", 0.0)
                done = result.get("done", False)
                error = None 

                rewards.append(reward)
                steps_taken = step
                last_reward = reward

                log_step(step=step, action=action_str, reward=reward, done=done, error=error)
                history.append(f"Step {step}: {action_str} -> reward {reward:+.2f}")

            # 3. Calculate Final Score 
            # In your physics env, max score is 1.0 per problem. We average the rewards.
            score = sum(rewards) / len(rewards) if rewards else 0.0 
            score = min(max(score, 0.0), 1.0)  
            success = score >= SUCCESS_SCORE_THRESHOLD

    except Exception as e:
        print(f"[DEBUG] Execution error: {e}", flush=True)
    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


if __name__ == "__main__":
    asyncio.run(main())
