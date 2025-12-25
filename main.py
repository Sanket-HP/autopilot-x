from fastapi import FastAPI
from pydantic import BaseModel

from brain.chronosense import ChronoSense
from brain.signalscore import SignalScore
from brain.ruleweave import RuleWeave
from brain.priorityflux import PriorityFlux
from brain.autotrigger import AutoTrigger
from brain.explainlog import generate_log

from firebase.db import save_log

app = FastAPI(title="AutoPilot-X AI Brain", version="1.0.0")

# Initialize Brain Modules
chrono = ChronoSense(threshold_seconds=5)
signal_engine = SignalScore()
rule_engine = RuleWeave()
priority_engine = PriorityFlux()
auto_trigger = AutoTrigger()

# -----------------------------
# Input Schema
# -----------------------------
class InputData(BaseModel):
    cpu_usage: int


# -----------------------------
# Simulation Endpoint
# -----------------------------
@app.post("/simulate")
def simulate(data: InputData):
    cpu = data.cpu_usage

    # 1️⃣ ChronoSense – Time Intelligence
    chrono_result = chrono.evaluate(cpu > 80)
    time_valid = chrono_result["valid"]

    # 2️⃣ SignalScore – Severity Intelligence
    score_result = signal_engine.calculate(
        severity=cpu,
        frequency=2,
        duration=3
    )
    score = score_result["score"]

    # 3️⃣ RuleWeave – Decision Logic
    rule_result = rule_engine.decide(score, time_valid)
    decision = rule_result["decision"]

    if decision:
        # Possible actions
        actions = [
            {"name": "Send Alert", "priority": 3},
            {"name": "Scale Resources", "priority": 5}
        ]

        # 4️⃣ PriorityFlux – Conflict Resolution
        chosen_action = priority_engine.resolve(actions)

        # 5️⃣ AutoTrigger – Execute Action
        execution_result = auto_trigger.execute(chosen_action["name"])

        # 6️⃣ ExplainLog – Explainable AI Log
        log = generate_log(
            reason=f"CPU {cpu}% exceeded adaptive threshold",
            decision=chosen_action["name"],
            algorithms_used=[
                "ChronoSense",
                "SignalScore",
                "RuleWeave",
                "PriorityFlux",
                "AutoTrigger"
            ],
            input_snapshot={
                "cpu_usage": cpu,
                "signal_score": score
            }
        )

        # Save log to Firebase
        save_log(log)

        return {
            "status": "TRIGGERED",
            "action": execution_result,
            "decision_details": rule_result,
            "chrono_details": chrono_result,
            "score_details": score_result,
            "log": log
        }

    # If not triggered
    return {
        "status": "MONITORING",
        "cpu": cpu,
        "chrono_details": chrono_result,
        "score_details": score_result,
        "decision_details": rule_result
    }
