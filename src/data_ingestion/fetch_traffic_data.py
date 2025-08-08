import requests
import os
import csv
import dropbox
from datetime import datetime
from googlemaps import Client
from src.config.settings import GMAPS_API_KEY, DROBOX_API_KEY

gmaps = Client(key=GMAPS_API_KEY)
dbx = dropbox.Dropbox(DROBOX_API_KEY)

locations = [
    ("Universitas Gadjah Mada, Yogyakarta", "Stasiun Lempuyangan, Yogyakarta"),
    ("Universitas Gadjah Mada, Yogyakarta", "Stasiun Tugu, Yogyakarta"),
    ("Universitas Gadjah Mada, Yogyakarta", "Tugu Jogja, Yogyakarta"),
    ("Universitas Gadjah Mada, Yogyakarta", "Malioboro, Yogyakarta"),
    ("Universitas Gadjah Mada, Yogyakarta", "Kota Gede, Yogyakarta"),
    ("Universitas Gadjah Mada, Yogyakarta", "Prawirotaman, Yogyakarta"),
]

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
        now = datetime.now()
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

def save_to_csv(data, filename):
    """Simpan ke CSV sementara lalu upload ke Dropbox"""
    if data is None:
        return

    tmp_path = f"/tmp/{filename}"
    all_rows = []

    # 1️⃣ Ambil data lama dari Dropbox
    try:
        metadata, res = dbx.files_download(f"/{filename}")
        content = res.content.decode("utf-8").splitlines()
        reader = csv.DictReader(content)
        all_rows.extend(reader)
        print(f"📥 Data lama ditemukan: {len(all_rows)} baris")
    except dropbox.exceptions.ApiError:
        print("ℹ️ Tidak ada file lama di Dropbox, mulai dari kosong.")

    all_rows.append(data)

    unique_rows = {}
    for row in all_rows:
        key = (row["timestamp"], row["origin"], row["destination"])
        unique_rows[key] = row  # overwrite jika ada yang sama

    with open(tmp_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        writer.writeheader()
        writer.writerows(unique_rows.values())

    # Upload ke Dropbox (overwrite jika sudah ada)
    with open(tmp_path, "rb") as f:
        dbx.files_upload(
            f.read(),
            f"/{filename}",  # lokasi di Dropbox
            mode=dropbox.files.WriteMode("overwrite")
        )
    print(f"✅ File {filename} berhasil diupload ke Dropbox.")
