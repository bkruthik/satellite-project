import requests

API_KEY = "883fb6619a910642a9fc73268e33ad75bc511a27"

def get_real_aqi(city):
    try:
        url = f"https://api.waqi.info/feed/{city}/?token={API_KEY}"
        
        # 🔥 ADDED timeout (prevents hanging)
        res = requests.get(url, timeout=5)

        # 🔥 ADDED safety check
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