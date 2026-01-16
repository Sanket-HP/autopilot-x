import time
import psutil
import requests

URL = "http://127.0.0.1:8000/ingest"

print("[Agent] Live telemetry agent started")

while True:
    cpu = psutil.cpu_percent(interval=1)
    requests.post(URL, json={"cpu_usage": int(cpu)})
    time.sleep(4)
