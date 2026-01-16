from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from datetime import datetime

from brain.chronosense import ChronoSense
from brain.signalscore import SignalScore
from brain.ruleweave import RuleWeave
from brain.priorityflux import PriorityFlux
from brain.autotrigger import AutoTrigger
from brain.explainlog import generate_log

from brain.driftguard import DriftGuard
from brain.confidencegate import ConfidenceGate

# Firebase (optional)
try:
    from firebase.db import save_log
    FIREBASE_ENABLED = True
except Exception:
    FIREBASE_ENABLED = False

import uvicorn

print("[Main] AutoPilot-X starting...")

app = FastAPI(title="AutoPilot-X Autonomous Decision Brain")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Brain Modules
# -----------------------
chrono = ChronoSense(threshold_seconds=5)
signal_score = SignalScore()
rule_engine = RuleWeave()
priority_engine = PriorityFlux()
auto_trigger = AutoTrigger()

drift_guard = DriftGuard(window_size=5)
confidence_gate = ConfidenceGate(min_confidence=0.7)

# -----------------------
# GLOBAL STATE
# -----------------------
LATEST_STATE = {}

# -----------------------
# Models
# -----------------------
class InputData(BaseModel):
    cpu_usage: int


@app.get("/")
def health():
    return {"status": "AutoPilot-X running"}


@app.post("/simulate")
def simulate(data: InputData):
    return process_signal(data.cpu_usage, source="manual")


@app.post("/ingest")
def ingest(data: InputData):
    return process_signal(data.cpu_usage, source="telemetry")


@app.get("/latest")
def latest():
    return LATEST_STATE


# -----------------------
# CORE DECISION PIPELINE
# -----------------------
def process_signal(cpu: int, source: str):
    global LATEST_STATE

    # 1. Normalize
    inference_score = round(cpu / 100, 3)

    # 2. Time persistence
    persistence = chrono.evaluate(cpu > 80)

    # 3. Signal scoring
    score_data = signal_score.calculate(
        severity=cpu,
        frequency=2,
        duration=3
    )

    # 4. Drift detection
    drift_data = drift_guard.update(cpu)

    # 5. Rule evaluation
    rule_data = rule_engine.decide(inference_score, persistence)

    # 6. Confidence gating
    confidence_data = confidence_gate.evaluate(
        score=inference_score,
        persistence=persistence
    )

    # -----------------------
    # Decision Resolution
    # -----------------------
    explainability = []

    if inference_score >= 0.75:
        status = "CRITICAL"
        decision = "AUTO_MITIGATE"
        explainability.append("CPU exceeds critical threshold (75%)")
    elif inference_score >= 0.55:
        status = "WARNING"
        decision = "THROTTLE"
        explainability.append("CPU exceeds warning threshold (55%)")
    else:
        status = "STABLE"
        decision = "NO_ACTION"
        explainability.append("CPU within safe operating range")

    explainability.append(f"Observed CPU load: {cpu}%")
    explainability.append(f"Confidence score: {confidence_data['confidence']}")
    explainability.append(f"Drift detected: {drift_data.get('drift_detected')}")

    # Optional auto-trigger
    action_result = None
    if decision != "NO_ACTION" and confidence_data["allowed"]:
        action_result = auto_trigger.execute(decision)
        explainability.append(f"Action executed: {decision}")

    log = generate_log(
        f"[{source}] CPU={cpu}% | Score={inference_score} | Status={status}"
    )

    if FIREBASE_ENABLED:
        save_log(log)

    response = {
        "agent_id": "XP-990-ALPHA",
        "timestamp": datetime.utcnow().isoformat(),
        "source": source,
        "cpu_raw": cpu,
        "inference_score": inference_score,
        "status": status,
        "decision": decision,
        "confidence": confidence_data["confidence"],
        "drift": drift_data,
        "explainability": explainability
    }

    LATEST_STATE = response
    return response


# -----------------------
# ENTRYPOINT
# -----------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"[Main] Launching AutoPilot-X on port {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port)
