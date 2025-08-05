import os
from dotenv import load_dotenv

load_dotenv(override=True)

GMAPS_API_KEY = os.getenv("GMAPS_API_KEY")
TRAFFIC_DATA_FILE = "src/data/traffic_data.csv"