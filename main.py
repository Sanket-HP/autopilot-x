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

app = FastAPI(title="AutoPilot-X AI Brain")

# ✅ CORS CONFIG (THIS FIXES YOUR ISSUE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for hackathon/demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Brain Modules
chrono = ChronoSense(threshold_seconds=5)
signal_score = SignalScore()
rule_engine = RuleWeave()
priority_engine = PriorityFlux()
auto_trigger = AutoTrigger()

class InputData(BaseModel):
    cpu_usage: int

@app.post("/simulate")
def simulate(data: InputData):
    cpu = data.cpu_usage

    time_valid = chrono.evaluate(cpu > 80)

    score = signal_score.calculate(
        severity=cpu,
        frequency=2,
        duration=3
    )

    decision = rule_engine.decide(score, time_valid)

    if decision:
        actions = [
            {"name": "Send Alert", "priority": 3},
            {"name": "Scale Resources", "priority": 5}
        ]

        chosen = priority_engine.resolve(actions)
        result = auto_trigger.execute(chosen["name"])

        log = generate_log(
            f"CPU {cpu}% exceeded threshold. Score={score}"
        )

        save_log(log)

        return {
            "status": "TRIGGERED",
            "decision": chosen["name"],
            "score": score,
            "log": log
        }

    return {
        "status": "MONITORING",
        "cpu": cpu,
        "score": score
    }
