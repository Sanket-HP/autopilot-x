import firebase_admin
from firebase_admin import credentials, db
import os
import json

firebase_enabled = False

# Try to load Firebase credentials safely
try:
    firebase_key = json.loads(os.environ.get("FIREBASE_SERVICE_ACCOUNT", ""))
    firebase_db_url = os.environ.get("FIREBASE_DB_URL")

    if firebase_key and firebase_db_url:
        cred = credentials.Certificate(firebase_key)
        firebase_admin.initialize_app(cred, {
            "databaseURL": firebase_db_url
        })
        firebase_enabled = True
        print("[Firebase] Connected successfully")
    else:
        print("[Firebase] Environment variables not set. Running in local mode.")

except Exception as e:
    print(f"[Firebase] Disabled due to error: {e}")
    firebase_enabled = False


def save_log(data: dict):
    if not firebase_enabled:
        print("[LocalLog]", data)
        return

    ref = db.reference("logs")
    ref.push(data)
