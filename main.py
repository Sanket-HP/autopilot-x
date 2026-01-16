from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from brain.chronosense import ChronoSense
from brain.signalscore import SignalScore
from brain.ruleweave import RuleWeave
from brain.priorityflux import PriorityFlux
from brain.autotrigger import AutoTrigger
from brain.explainlog import generate_log

# Intelligence layers
from brain.driftguard import DriftGuard
from brain.confidencegate import ConfidenceGate

# Firebase (optional, safe for cloud)
try:
    from firebase.db import save_log
    FIREBASE_ENABLED = True
except Exception:
    FIREBASE_ENABLED = False

import uvicorn

print("[Main] AutoPilot-X starting...")

app = FastAPI(title="AutoPilot-X Autonomous Decision Brain")

# CORS (cloud + firebase safe)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core brain modules
chrono = ChronoSense(threshold_seconds=5)
signal_score = SignalScore()
rule_engine = RuleWeave()
priority_engine = PriorityFlux()
auto_trigger = AutoTrigger()

# Intelligence layers
drift_guard = DriftGuard(window_size=5)
confidence_gate = ConfidenceGate(min_confidence=0.7)

# 🔹 GLOBAL LIVE STATE (for dashboard polling)
LATEST_STATE = {}


class InputData(BaseModel):
    cpu_usage: int


@app.get("/")
def health_check():
    return {
        "status": "AutoPilot-X running",
        "mode": "Live / Offline / Cloud-ready"
    }


# 🔹 Manual UI simulation
@app.post("/simulate")
def simulate(data: InputData):
    return process_signal(data.cpu_usage, source="UI")


# 🔹 Real-time telemetry ingestion (agents, laptops, cloud)
@app.post("/ingest")
def ingest(data: InputData):
    return process_signal(data.cpu_usage, source="Telemetry")


# 🔹 Dashboard polling endpoint
@app.get("/latest")
def latest_state():
    return LATEST_STATE


# 🔹 Shared decision pipeline
def process_signal(cpu: int, source: str):
    global LATEST_STATE

    print(f"[{source}] CPU signal received: {cpu}%")

    # 1. Time persistence
    time_valid = chrono.evaluate(cpu > 80)

    # 2. Signal scoring
    score_data = signal_score.calculate(
        severity=cpu,
        frequency=2,
        duration=3
    )
    score_value = score_data["score"]

    # 3. Drift detection
    drift_data = drift_guard.update(cpu)

    # 4. Rule evaluation
    decision_data = rule_engine.decide(score_value, time_valid)

    # 5. Confidence gating
    confidence_data = confidence_gate.evaluate(
        score=score_value,
        persistence=time_valid
    )

    # 6. Decision resolution
    if decision_data["decision"] and confidence_data["allowed"]:
        actions = [
            {"name": "Send Alert", "priority": 3},
            {"name": "Scale Resources", "priority": 5}
        ]

        chosen = priority_engine.resolve(actions)
        action_result = auto_trigger.execute(chosen["name"])

        log = generate_log(
            f"[{source}] CPU={cpu}% | Score={score_value} | Drift={drift_data.get('drift_detected')} | Confidence={confidence_data['confidence']}"
        )

        if FIREBASE_ENABLED:
            save_log(log)

        response = {
            "status": "TRIGGERED",
            "source": source,
            "decision": chosen["name"],
            "confidence": confidence_data,
            "drift_analysis": drift_data,
            "score": score_value,
            "signal_analysis": score_data,
            "rule_analysis": decision_data,
            "action": action_result,
            "log": log
        }

        LATEST_STATE = response
        return response

    # Monitoring state
    response = {
        "status": "MONITORING",
        "source": source,
        "cpu": cpu,
        "confidence": confidence_data,
        "drift_analysis": drift_data,
        "score": score_value,
        "signal_analysis": score_data,
        "rule_analysis": decision_data
    }

    LATEST_STATE = response
    return response


# ✅ CLOUD-SAFE ENTRYPOINT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"[Main] Launching AutoPilot-X on port {port}")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port
    )
