# 🌍 AI-Based Land Cover and Environmental Risk Analysis

An AI-powered environmental analysis system that combines satellite imagery from Google Earth Engine (GEE) with Machine Learning to analyze environmental conditions of user-selected locations. The system provides insights into vegetation health, urbanization, water presence, air quality, and environmental risk levels.

---

## 📖 Table of Contents

* Overview
* Features
* System Architecture
* Machine Learning Workflow
* Tech Stack
* Project Structure
* Installation & Setup
* API Reference
* Evaluation Metrics
* Future Improvements

---

## 🚀 Overview

This system utilizes Sentinel-2 satellite imagery, NDVI (Normalized Difference Vegetation Index) analysis, and a Random Forest Machine Learning model to provide:

* Real-time environmental analysis
* Land cover distribution analysis
* Environmental risk prediction with confidence scores
* Future environmental risk estimation
* Air Quality Index (AQI) monitoring
* Interactive visualizations and charts

---

## ✨ Features

### 🛰️ Satellite Data Analysis

* Fetches Sentinel-2 imagery using Google Earth Engine (GEE)
* Computes NDVI values for vegetation health assessment
* Applies cloud filtering for improved accuracy

### 📍 Multi-Point Environmental Analysis

* Samples multiple nearby geographic locations
* Reduces localized measurement errors
* Produces balanced environmental representations

### 🌱 Land Cover Analysis

Estimates percentage distribution of:

* Vegetation
* Urban Areas
* Water Bodies
* Bare Land

### 🤖 Machine Learning Prediction

* Uses a Random Forest Classifier
* Predicts environmental risk levels:

  * Low
  * Medium
  * High
* Generates confidence scores for predictions

### ⚠️ Environmental Risk Detection

Identifies environmental concerns such as:

* Urban Heat Island Effect
* Vegetation Loss
* Water Scarcity

### 🔮 Future Prediction

Forecasts future environmental conditions based on:

* Urban growth trends
* Vegetation reduction patterns
* Historical environmental trends

### 🌫️ Air Quality Analysis

Fetches real-time pollution data including:

* AQI
* PM2.5
* PM10
* Overall pollution levels

### 📊 Data Visualization

Displays results using:

* Pie Charts
* Bar Charts
* Satellite Imagery
* AQI Indicators
* Environmental Risk Metrics

---

## 🏗️ System Architecture

```text
User Input
    │
    ▼
Frontend (React UI)
    │
    ▼
FastAPI Backend
    │
    ▼
Google Earth Engine + AQI APIs
    │
    ▼
NDVI & Land Cover Extraction
    │
    ▼
Machine Learning Prediction
    │
    ▼
Risk Analysis & Future Prediction
    │
    ▼
Visualization & Results
```

---

## 🧠 Machine Learning Workflow

1. Environmental features are extracted and preprocessed.
2. Features include:

   * NDVI
   * Urban Area Percentage
   * Water Coverage
   * Bare Land Coverage
3. A Random Forest model is trained on environmental scenarios.
4. The model predicts environmental risk levels.
5. Performance is evaluated using:

   * Accuracy
   * Precision
   * Recall
   * F1 Score

### Cloud Filtering

Satellite imagery often contains cloud-covered pixels that can distort NDVI calculations. Cloud filtering removes these pixels before analysis, ensuring more reliable environmental assessments.

---

## 🛠️ Tech Stack

| Layer                 | Technologies                                       |
| --------------------- | -------------------------------------------------- |
| Frontend              | React.js, Tailwind CSS, Axios, Recharts / Chart.js |
| Backend               | FastAPI, Python                                    |
| Machine Learning      | Scikit-learn, Random Forest Classifier, NumPy      |
| Geospatial Processing | Google Earth Engine (GEE), Sentinel-2              |
| APIs                  | WAQI API, AQI API, Geocoding API                   |

---

## 📂 Project Structure

```text
satellite-app/
│
├── backend/
│   ├── main.py
│   ├── gee_ndvi.py
│   ├── gee_air_pollution.py
│   ├── geocoder.py
│   ├── aqi_api.py
│   ├── waqi_api.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── App.jsx
│   └── package.json
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd satellite-app
```

### 2. Backend Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

### 3. Frontend Setup

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

## 🔗 API Reference

### Health Check

```http
GET /
```

### Analyze Environmental Data

```http
POST /analyze
```

### Request Body

```json
{
  "continent": "Asia",
  "country": "India",
  "city": "Hyderabad",
  "start_date": "2026-03-01",
  "end_date": "2026-03-25"
}
```

### Response Includes

| Field              | Description                                      |
| ------------------ | ------------------------------------------------ |
| ndvi               | NDVI value for the selected region               |
| risk_level         | Predicted environmental risk level               |
| ml_prediction      | Machine learning prediction                      |
| confidence_score   | Prediction confidence percentage                 |
| land_cover         | Vegetation, Urban, Water, Bare Land distribution |
| aqi_info           | AQI and pollutant information                    |
| detected_risks     | Identified environmental risks                   |
| suggestions        | Recommended actions                              |
| future_prediction  | Estimated future environmental conditions        |
| evaluation_metrics | Accuracy, Precision, Recall, F1 Score            |
| satellite_image    | Processed satellite imagery                      |

---

## 📈 Evaluation Metrics

Model performance is evaluated using:

| Metric    | Description                           |
| --------- | ------------------------------------- |
| Accuracy  | Overall prediction correctness        |
| Precision | Correctness of positive predictions   |
| Recall    | Coverage of actual positive cases     |
| F1 Score  | Harmonic mean of Precision and Recall |

---

## 🔮 Future Improvements

* Integration with larger environmental datasets
* Advanced Deep Learning models for improved accuracy
* Time-series forecasting and trend analysis
* Live environmental monitoring dashboard
* Large-scale geographic analysis support
* Mobile application development

---

## 🚀 Built With

* Python
* FastAPI
* React.js
* Google Earth Engine
* Scikit-learn
* Sentinel-2 Satellite Data

---

## 👨‍💻 Author

Developed as a learning project to explore Geospatial Analysis, Machine Learning, Environmental Monitoring, and Full-Stack Development using React, FastAPI, and Google Earth Engine.
