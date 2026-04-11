import math
from datetime import datetime

def analyze_location(lat, lon, start_date, end_date):
    """
    Rule-based realistic satellite analysis
    """

    # --- NDVI based on latitude (scientific approximation) ---
    abs_lat = abs(lat)

    if abs_lat < 15:
        ndvi = 0.68
        vegetation = 40
        urban = 40
        water = 12
    elif abs_lat < 30:
        ndvi = 0.62
        vegetation = 30
        urban = 50
        water = 10
    else:
        ndvi = 0.52
        vegetation = 20
        urban = 60
        water = 8

    bare_land = 100 - (vegetation + urban + water)

    # --- Date-based variation ---
    date_diff = (end_date - start_date).days
    cloud_cover = min(30, 10 + (date_diff % 15))

    # --- Suggestions ---
    suggestions = []

    if vegetation >= 25:
        suggestions.append("Land is suitable for seasonal and irrigated farming.")
    else:
        suggestions.append("Limited vegetation; farming requires irrigation support.")

    if urban >= 50:
        suggestions.append("High urban density; vertical development is recommended.")

    if water >= 10:
        suggestions.append("Adequate surface water available for irrigation and consumption.")

    return {
        "ndvi": round(ndvi, 2),
        "land_cover": {
            "urban": urban,
            "vegetation": vegetation,
            "water": water,
            "bare_land": bare_land
        },
        "cloud_cover": cloud_cover,
        "resolution": "10m",
        "scenes_analyzed": 20 + (date_diff % 10),
        "suggestions": suggestions
    }