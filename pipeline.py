from src.config.settings import TRAFFIC_DATA_FILE
from src.data_ingestion.fetch_traffic_data import fetch_traffic, save_to_csv, locations

if __name__ == "__main__":
    for origin, destination in locations:
        traffic_data = fetch_traffic(origin, destination)
        save_to_csv(traffic_data, TRAFFIC_DATA_FILE)
        print(f"Data saved for {origin} to {destination}: {traffic_data}")