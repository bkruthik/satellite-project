from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ee
import numpy as np
import random

from aqi_api import get_real_time_aqi
from waqi_api import get_real_aqi
from geocoder import get_coordinates
from gee_ndvi import get_ndvi_and_rgb
from gee_air_pollution import get_air_pollution

# ML
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

ee.Initialize()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    continent: str
    country: str
    city: str
    start_date: str
    end_date: str

# ================= REALISTIC ML MODEL =================

random.seed(42)
np.random.seed(42)

X = []
y = []

for i in range(500):
    ndvi = random.uniform(0.05, 0.9)
    ndvi += random.uniform(-0.05, 0.05)  # noise

    urban = random.randint(10, 90)
    water = random.randint(1, 30)
    bare = random.randint(5, 40)

    X.append([ndvi, urban, water, bare])

    # better logic
    if ndvi > 0.6 and urban < 40:
        label = "Low"
    elif ndvi > 0.35:
        label = "Medium"
    else:
        label = "High"

    # add 10% randomness
    if random.random() < 0.1:
        label = random.choice(["Low", "Medium", "High"])

    y.append(label)

X = np.array(X)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", round(accuracy * 100, 2), "%")

# ================= ROUTES =================

@app.get("/")
def health():
    return {
        "status": "Backend running",
        "source": "Google Earth Engine (Sentinel-2)"
    }

@app.get("/aqi/{city}")
def get_aqi_city(city: str):
    return get_real_aqi(city)

@app.post("/analyze")
def analyze(req: AnalysisRequest):

    lat, lon = get_coordinates(req.city, req.country)

    points = [
        (lat, lon),
        (lat + 0.05, lon),
        (lat - 0.05, lon),
        (lat, lon + 0.05),
        (lat, lon - 0.05)
    ]

    ndvi_list, urban_list, water_list, bare_list = [], [], [], []
    satellite_image_url = None
    pollution_data = None

    for p_lat, p_lon in points:

        geometry = ee.Geometry.Point([p_lon, p_lat]).buffer(5000)

        gee_result = get_ndvi_and_rgb(
            geometry,
            req.start_date,
            req.end_date
        )

        if gee_result is None:
            continue

        ndvi = float(gee_result["ndvi"])

        if satellite_image_url is None:
            satellite_image_url = gee_result["rgb_url"]

        vegetation = int(max(0, min(1, ndvi)) * 100)

        bare_land = int((0.15 - ndvi) * 100) if ndvi < 0.15 else 5
        water = gee_result.get("water", 0)
        urban = max(0, 100 - (vegetation + water + bare_land))

        ndvi_list.append(ndvi)
        urban_list.append(urban)
        water_list.append(water)
        bare_list.append(bare_land)

        if pollution_data is None:
            pollution_data = get_air_pollution(
                geometry,
                req.start_date,
                req.end_date
            )

    if not ndvi_list:
        return {"success": False, "error": "No satellite data"}

    # AVERAGE
    ndvi = round(sum(ndvi_list) / len(ndvi_list), 4)
    urban = int(sum(urban_list) / len(urban_list))
    water = int(sum(water_list) / len(water_list))
    bare_land = int(sum(bare_list) / len(bare_list))
    vegetation = int(max(0, min(1, ndvi)) * 100)

    # AQI
    aqi_data = get_real_time_aqi(lat, lon)
    real_aqi = get_real_aqi(req.city)

    # BASIC RISK
    if ndvi > 0.6:
        risk = "Low"
    elif ndvi > 0.3:
        risk = "Medium"
    else:
        risk = "High"

    # ================= ML PREDICTION =================
    input_data = np.array([[ndvi, urban, water, bare_land]])
    ml_prediction = model.predict(input_data)[0]
    ml_confidence = round(model.predict_proba(input_data).max() * 100, 2)

    # ================= DETECTED RISKS =================
    detected_risks = []
    suggestions = []

    if urban > 50:
        detected_risks.append("Urban Heat Island")
        suggestions.append("Increase green cover")

    if ndvi < 0.3:
        detected_risks.append("Vegetation Loss")
        suggestions.append("Plant more trees")

    if water < 15:
        detected_risks.append("Water Scarcity")
        suggestions.append("Improve water conservation")

    if not detected_risks:
        detected_risks = ["No major risks detected"]

    if not suggestions:
        suggestions = ["Maintain current conditions"]

    # ================= FUTURE PREDICTION =================
    future_urban = urban + 15
    future_vegetation = max(0, vegetation - 20)

    future_score = (
        future_urban * 0.4 +
        bare_land * 0.3 +
        (1 - ndvi) * 100 * 0.3
    )

    if future_score < 40:
        future_level = "Low"
    elif future_score < 70:
        future_level = "Medium"
    else:
        future_level = "High"

    future_data = {
        "future_urban": round(future_urban, 2),
        "future_vegetation": round(future_vegetation, 2),
        "future_risk_score": round(future_score, 2),
        "future_risk_level": future_level
    }

    # ================= RESPONSE =================
    return {
        "success": True,
        "location": f"{req.city}, {req.country}",
        "analysis": {
            "ndvi": ndvi,
            "risk": risk,

            "ml_prediction": ml_prediction,
            "ml_confidence": ml_confidence,

            "model_accuracy": float(round(accuracy * 100, 2)),

            "land_cover": {
                "vegetation": vegetation,
                "urban": urban,
                "water": water,
                "bare_land": bare_land
            },

            "detected_risks": detected_risks,
            "dynamic_suggestions": suggestions,
            "future_prediction": future_data,

            "air_pollution": pollution_data,
            "real_time_aqi": aqi_data,
            "real_aqi": real_aqi,

            "satellite_image_url": satellite_image_url
        }
    }