import firebase_admin
from firebase_admin import credentials, db
import os
import json

firebase_key = json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"])

cred = credentials.Certificate(firebase_key)

firebase_admin.initialize_app(cred, {
    "databaseURL": os.environ["FIREBASE_DB_URL"]
})

def save_log(data: dict):
    ref = db.reference("logs")
    ref.push(data)
