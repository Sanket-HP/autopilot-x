import time
import psutil
import requests

# =========================
# CONFIG
# =========================
URL = "https://autopilot-x.onrender.com/ingest"
AGENT_ID = "XP-990-ALPHA"
INTERVAL = 4  # seconds

print("[AutoPilot-X] Realtime Autonomous Agent Started")
print(f"[Agent-ID] {AGENT_ID}")

while True:
    try:
        # 1. Sense CPU
        cpu_raw = int(psutil.cpu_percent(interval=1))

        # 2. Send ONLY what backend expects
        payload = {
            "cpu_usage": cpu_raw
        }

        response = requests.post(URL, json=payload, timeout=5)

        if response.status_code == 200:
            print(f"[✓] Telemetry sent | CPU={cpu_raw}%")
        else:
            print(f"[!] Server error {response.status_code} | {response.text}")

    except Exception as e:
        print(f"[ERROR] {e}")

    time.sleep(INTERVAL)
