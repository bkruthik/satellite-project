import numpy as np
from sklearn.ensemble import RandomForestClassifier

# ================= TRAIN MODEL =================

X = [
    [0.8, 10, 20, 5],
    [0.7, 20, 18, 5],
    [0.6, 30, 15, 10],
    [0.5, 40, 12, 10],
    [0.4, 50, 10, 15],
    [0.3, 60, 8, 20],
    [0.2, 70, 5, 25],
    [0.1, 80, 3, 30],
]

y = ["Low", "Low", "Medium", "Medium", "Medium", "High", "High", "High"]

model = RandomForestClassifier(n_estimators=150, random_state=42)
model.fit(X, y)

# ================= FUNCTIONS =================

def predict_risk_ml(ndvi, urban, water, bare_land):
    data = np.array([[ndvi, urban, water, bare_land]])
    pred = model.predict(data)[0]
    conf = model.predict_proba(data).max()
    return pred, round(conf * 100, 2)


def dynamic_analysis(ndvi, urban, vegetation, water, bare_land):
    risks = []
    suggestions = []

    if urban > 50:
        risks.append("Urban Heat Island")
        suggestions.append("Increase green cover")

    if ndvi < 0.3:
        risks.append("Vegetation Loss")
        suggestions.append("Afforestation needed")

    if water < 12:
        risks.append("Water Scarcity")
        suggestions.append("Rainwater harvesting")

    return risks, suggestions


def future_prediction(ndvi, urban, vegetation, water, bare_land, years=10):
    future_urban = urban + (years * 1.5)
    future_vegetation = max(0, vegetation - (years * 1.2))

    score = (
        future_urban * 0.35 +
        bare_land * 0.25 +
        (1 - ndvi) * 100 * 0.20 +
        (20 - water) * 0.20
    )

    level = "Low" if score < 40 else "Medium" if score < 70 else "High"

    return {
        "future_urban": round(future_urban, 2),
        "future_vegetation": round(future_vegetation, 2),
        "future_risk_score": round(score, 2),
        "future_risk_level": level
    }