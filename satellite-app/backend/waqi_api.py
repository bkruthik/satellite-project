import requests
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Get API key securely
API_KEY = os.getenv("WAQI_API_KEY")

def get_real_aqi(city):
    try:
        url = f"https://api.waqi.info/feed/{city}/?token={API_KEY}"

        # Prevent hanging
        res = requests.get(url, timeout=5)

        # Safety check
        if res.status_code != 200:
            return {"error": "WAQI API failed"}

        data = res.json()

        if data["status"] != "ok":
            return {"error": "AQI data not available"}

        return {
            "aqi": data["data"]["aqi"],
            "city": data["data"]["city"]["name"]
        }

    except Exception as e:
        return {"error": str(e)}
