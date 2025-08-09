import requests
import json
import firebase_admin
from datetime import datetime
from zoneinfo import ZoneInfo
from googlemaps import Client
from src.config.settings import GMAPS_API_KEY, FIREBASE_CONFIG
from firebase_admin import credentials, firestore

gmaps = Client(key=GMAPS_API_KEY)
firebase_key_dict = json.loads(FIREBASE_CONFIG)

cred = credentials.Certificate(firebase_key_dict)
firebase_admin.initialize_app(cred)
db = firestore.client()

locations = [
    ("Universitas Gadjah Mada, Yogyakarta", "Stasiun Lempuyangan, Yogyakarta"),
    ("Universitas Gadjah Mada, Yogyakarta", "Stasiun Tugu, Yogyakarta"),
    ("Universitas Gadjah Mada, Yogyakarta", "Tugu Jogja, Yogyakarta"),
    ("Universitas Gadjah Mada, Yogyakarta", "Malioboro, Yogyakarta"),
    ("Universitas Gadjah Mada, Yogyakarta", "Kota Gede, Yogyakarta"),
    ("Universitas Gadjah Mada, Yogyakarta", "Prawirotaman, Yogyakarta"),
]

def get_wib_time():
    return datetime.now(ZoneInfo("Asia/Jakarta"))

def enrich_time_features(ts: datetime):
    return {
        "hour": ts.hour,
        "minute": ts.minute,
        "day_of_week": ts.weekday(),  # 0 = Monday
        "is_weekend": ts.weekday() >= 5
    }

def fetch_traffic(origin, destination):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "departure_time": "now",
        "key": GMAPS_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    try:
        leg = data['routes'][0]['legs'][0]
        now = get_wib_time()
        time_features = enrich_time_features(now)

        duration = leg['duration']['value']
        duration_traffic = leg.get('duration_in_traffic', {}).get('value', None)
        delay = duration_traffic - duration if duration_traffic is not None else None

        return {
            "timestamp": now.isoformat(),
            "origin": origin,
            "destination": destination,
            "distance_meters": leg['distance']['value'],
            "duration_seconds": duration,
            "duration_traffic_seconds": duration_traffic,
            "traffic_delay": delay,
            **time_features  # merge waktu ke dict
        }

    except (KeyError, IndexError) as e:
        print(f"Error fetching route from {origin} to {destination}: {e}")
        return None
    

def save_to_firestore_batch(data_list):
    batch = db.batch()
    for data in data_list:
        doc_id = f"{data['timestamp']}_{data['origin']}_{data['destination']}"
        doc_id = doc_id.replace(" ", "_").replace(":", "-")
        doc_ref = db.collection("traffic_data").document(doc_id)
        batch.set(doc_ref, data)
    batch.commit()
