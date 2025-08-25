from src.config.settings import TRAFFIC_DATA_FILE
from src.data_ingestion.fetch_traffic_data import fetch_traffic, locations
from flask import Flask, jsonify
from src.data_ingestion.firestore_utils import save_to_firestore_batch
from src.data_export.extract_csv import extract_csv

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "API is running"}), 200

@app.route('/fetch-traffic', methods=['GET'])
def fetch_all():
    all_data = []
    for origin, destination in locations:
        data = fetch_traffic(origin, destination)
        if data:
            all_data.append(data)

    save_to_firestore_batch(all_data)
    return jsonify(all_data), 200

@app.route('/export-csv', methods=['GET'])
def export_csv():
    extract_csv()
    return jsonify({"message": "CSV exported successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090)
    