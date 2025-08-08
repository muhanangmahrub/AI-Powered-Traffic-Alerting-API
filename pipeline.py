from src.config.settings import TRAFFIC_DATA_FILE
from src.data_ingestion.fetch_traffic_data import fetch_traffic, save_to_csv, locations
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "API is running"}), 200

@app.route('/fetch-traffic', methods=['GET'])
def fetch_all():
    results = []
    for origin, destination in locations:
        data = fetch_traffic(origin, destination)
        save_to_csv(data, "traffic_data.csv")
        if data:
            results.append(data)

    return jsonify(results), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090)