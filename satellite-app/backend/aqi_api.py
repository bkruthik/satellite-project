import requests

API_KEY=your_actual_key

def get_real_time_aqi(lat, lon):
    try:
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        
        response = requests.get(url)
        data = response.json()

        aqi = data["list"][0]["main"]["aqi"]
        components = data["list"][0]["components"]

        return {
            "aqi": aqi,
            "pm2_5": components["pm2_5"],
            "pm10": components["pm10"]
            
        }

    except Exception as e:
        return {"error": str(e)}
        
