import json
import firebase_admin
from src.config.settings import FIREBASE_CONFIG
from firebase_admin import credentials, firestore

firebase_key_dict = json.loads(FIREBASE_CONFIG)
cred = credentials.Certificate(firebase_key_dict)
firebase_admin.initialize_app(cred)
db = firestore.client()

def save_to_firestore_batch(data_list):
    batch = db.batch()
    for data in data_list:
        doc_id = f"{data['timestamp']}_{data['origin']}_{data['destination']}"
        doc_id = doc_id.replace(" ", "_").replace(":", "-")
        doc_ref = db.collection("traffic_data").document(doc_id)
        batch.set(doc_ref, data)
    batch.commit()

def get_all_documents(collection_name):
    docs = db.collection(collection_name).stream()
    return list(docs)