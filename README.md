🌍 AI-Based Land Cover and Environmental Risk Analysis
An AI-powered environmental analysis system that combines satellite imagery from Google Earth Engine (GEE) with Machine Learning to analyze environmental conditions of any user-selected location — providing real-time insights on vegetation, urbanization, water presence, air quality, and environmental risk.

**Table of Contents**


**Overview**:
   .Features
   .System Architecture
   .Machine Learning Workflow
   .Tech Stack
   .Project Structure
   .Installation & Setup
   .API Reference
   .Evaluation Metrics
   .Future Improvements


**Overview**
This system uses Sentinel-2 satellite data and NDVI (Normalized Difference Vegetation Index) analysis combined with a Random Forest ML model to deliver:

Real-time environmental analysis
Land cover distribution (vegetation, urban, water, bare land)
Environmental risk prediction with confidence scores
Future risk estimation
Air Quality Index (AQI) data
Visual charts and satellite imagery


**Features**

** Satellite Data Analysis**

Fetches Sentinel-2 imagery via Google Earth Engine
Computes NDVI values for vegetation health assessment
Applies cloud filtering for improved data accuracy

**Multi-Point Environmental Analysis**


Samples multiple nearby geographic points
Reduces localized measurement errors
Produces a balanced environmental representation

**Land Cover Analysis**

Estimates percentage distribution of:

Vegetation
Urban area
Water bodies
Bare land


**Machine Learning Prediction**

Random Forest Classifier predicts risk level: Low / Medium / High
Outputs a confidence score for each prediction

**Dynamic Environmental Risk Detection**
Identifies issues such as:

Urban Heat Island
Vegetation Loss
Water Scarcity

**Future Prediction**
Estimates future environmental conditions based on:

Urban growth trends
Vegetation reduction patterns
Environmental trend extrapolation

**Air Quality Analysis**

Fetches real-time data including:

AQI, PM2.5, PM10, and overall pollution levels

**Data Visualization**

Displays results via:

Pie charts & bar charts
Satellite imagery
AQI indicators
Risk metrics

**System Architecture**
User Input
   ↓
Frontend (React UI)
   ↓
FastAPI Backend
   ↓
Google Earth Engine + AQI APIs
   ↓
NDVI & Land Cover Extraction
   ↓
Machine Learning Prediction
   ↓
Risk Analysis & Future Prediction
   ↓
Visualization & Results

Machine Learning Workflow

Environmental feature values are generated and preprocessed
Features used: NDVI, Urban Area, Water, Bare Land
Random Forest model is trained on environmental scenarios
Model predicts environmental risk level
Performance is evaluated using Accuracy, Precision, Recall, and F1-Score


Cloud Filtering: Satellite images may contain clouds that distort NDVI values. Cloud filtering removes cloudy pixels before processing, ensuring only clear-sky observations are used.


**Tech Stack**
LayerTechnologiesFrontendReact.js, Tailwind CSS, Axios, Recharts / Chart.jsBackendFastAPI, PythonMachine LearningScikit-learn, Random Forest Classifier, NumPySatellite & GeospatialGoogle Earth Engine (GEE), Sentinel-2APIsWAQI API, AQI API, Geocoding API

Project Structure
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

**Installation & Setup**

1. Clone the Repository
bashgit clone <your-repository-link>
cd satellite-app
2. Backend Setup
bash# Install dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn main:app --reload
Backend runs at: http://127.0.0.1:8000
3. Frontend Setup
bash# Install packages
npm install

# Start the development server
npm run dev
Frontend runs at: http://localhost:5173

**API Reference**
Health Check
httpGET /
Analyze Environmental Data
httpPOST /analyze
Request Body:
json{
  "continent": "Asia",
  "country": "India",
  "city": "Hyderabad",
  "start_date": "2026-03-01",
  "end_date": "2026-03-25"
}
Response Includes:
FieldDescriptionndviNDVI value for the selected regionrisk_levelPredicted environmental risk levelml_predictionML model outputconfidence_scorePrediction confidence percentageland_coverVegetation / Urban / Water / Bare land distributionaqi_infoAir Quality Index and pollutant datadetected_risksList of identified environmental riskssuggestionsRecommended actionsfuture_predictionEstimated future environmental conditionsevaluation_metricsModel accuracy, precision, recall, F1-scoresatellite_imageRendered satellite imagery

Evaluation Metrics
Model performance is evaluated using:
MetricDescriptionAccuracyOverall correct predictionsPrecisionCorrectness of positive predictionsRecallCoverage of actual positive casesF1 ScoreHarmonic mean of precision and recall

**Future Improvements**

Integration with real-world environmental datasets
Advanced deep learning models for higher accuracy
Time-series prediction and trend analysis
Live environmental monitoring dashboard
Larger-scale geographic analysis support
Mobile application support


Built With

Python
FastAPI
React.js
Google Earth Engine
Scikit-learn
Sentinel-2 Satellite Data
