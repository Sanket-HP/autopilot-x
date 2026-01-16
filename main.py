from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from brain.chronosense import ChronoSense
from brain.signalscore import SignalScore
from brain.ruleweave import RuleWeave
from brain.priorityflux import PriorityFlux
from brain.autotrigger import AutoTrigger
from brain.explainlog import generate_log
from firebase.db import save_log

import uvicorn

print("[Main] AutoPilot-X starting...")

app = FastAPI(title="AutoPilot-X Autonomous Decision Brain")

# ✅ CORS CONFIG (hackathon-safe)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Initialize Brain Modules
chrono = ChronoSense(threshold_seconds=5)
signal_score = SignalScore()
rule_engine = RuleWeave()
priority_engine = PriorityFlux()
auto_trigger = AutoTrigger()


class InputData(BaseModel):
    cpu_usage: int


@app.get("/")
def health_check():
    return {
        "status": "AutoPilot-X running",
        "mode": "Local / Firebase-optional"
    }


@app.post("/simulate")
def simulate(data: InputData):
    cpu = data.cpu_usage
    print(f"[Simulate] Incoming CPU signal: {cpu}%")

    # Step 1: Temporal validation
    time_valid = chrono.evaluate(cpu > 80)
    print(f"[ChronoSense] Time valid = {time_valid}")

    # Step 2: Signal scoring
    score_data = signal_score.calculate(
        severity=cpu,
        frequency=2,
        duration=3
    )
    score_value = score_data["score"]
    print(f"[SignalScore] Score = {score_value}")

    # Step 3: Rule evaluation
    decision_data = rule_engine.decide(score_value, time_valid)
    print(f"[RuleWeave] Decision = {decision_data}")

    # Step 4: Decision handling
    if decision_data["decision"]:
        actions = [
            {"name": "Send Alert", "priority": 3},
            {"name": "Scale Resources", "priority": 5}
        ]

        chosen = priority_engine.resolve(actions)
        print(f"[PriorityFlux] Chosen action = {chosen}")

        action_result = auto_trigger.execute(chosen["name"])
        print(f"[AutoTrigger] Executed = {action_result}")

        log = generate_log(
            f"CPU {cpu}% exceeded threshold. Score={score_value}"
        )

        save_log(log)

        print("[ExplainLog] Log generated")

        return {
            "status": "TRIGGERED",
            "decision": chosen["name"],
            "score": score_value,
            "signal_analysis": score_data,
            "rule_analysis": decision_data,
            "action": action_result,
            "log": log
        }

    print("[Monitor] No trigger condition met")

    return {
        "status": "MONITORING",
        "cpu": cpu,
        "score": score_value,
        "signal_analysis": score_data,
        "rule_analysis": decision_data
    }


# ▶️ Allow direct execution: python main.py
if __name__ == "__main__":
    print("[Main] Launching FastAPI server on http://127.0.0.1:8000")
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )
