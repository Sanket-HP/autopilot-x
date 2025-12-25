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

# ✅ CORS CONFIG (for browser + demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hackathon-safe
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

    # Step 1: Temporal validation
    time_valid = chrono.evaluate(cpu > 80)

    # Step 2: Signal scoring (returns dict)
    score_data = signal_score.calculate(
        severity=cpu,
        frequency=2,
        duration=3
    )

    score_value = score_data["score"]

    # Step 3: Rule evaluation (returns dict)
    decision_data = rule_engine.decide(score_value, time_valid)

    # Step 4: Decision handling
    if decision_data["decision"]:
        actions = [
            {"name": "Send Alert", "priority": 3},
            {"name": "Scale Resources", "priority": 5}
        ]

        chosen = priority_engine.resolve(actions)
        action_result = auto_trigger.execute(chosen["name"])

        log = generate_log(
            f"CPU {cpu}% exceeded threshold. Score={score_value}"
        )

        save_log(log)

        return {
            "status": "TRIGGERED",
            "decision": chosen["name"],
            "score": score_value,
            "signal_analysis": score_data,
            "rule_analysis": decision_data,
            "action": action_result,
            "log": log
        }

    # Monitoring state
    return {
        "status": "MONITORING",
        "cpu": cpu,
        "score": score_value,
        "signal_analysis": score_data,
        "rule_analysis": decision_data
    }
