import { useState } from "react";
import LandCoverChart from "./components/LandCoverChart";
import LandCoverPie from "./components/LandCoverPie";
import "./App.css";
const DATA = {
  Asia: {
    India: ["Hyderabad", "Delhi", "Mumbai", "Bangalore"],
    China: ["Beijing", "Shanghai"],
    Japan: ["Tokyo", "Osaka"],
  },
  Africa: {
    Nigeria: ["Lagos", "Abuja"],
    Egypt: ["Cairo", "Alexandria"],
  },
  Europe: {
    Germany: ["Berlin", "Munich"],
    France: ["Paris", "Lyon"],
  },
  "North America": {
    USA: ["New York", "Los Angeles"],
    Canada: ["Toronto", "Vancouver"],
  },
  "South America": {
    Brazil: ["São Paulo", "Rio de Janeiro"],
  },
  Oceania: {
    Australia: ["Sydney", "Melbourne"],
  },
};

export default function App() {

  const [stage, setStage] = useState("title");
  const [continent, setContinent] = useState("");
  const [country, setCountry] = useState("");
  const [city, setCity] = useState("");

  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const [graphView, setGraphView] = useState(null);

  const [showLand, setShowLand] = useState(false);
  const [showRisk, setShowRisk] = useState(false);
  const [showSuggest, setShowSuggest] = useState(false);
  const [showFuture, setShowFuture] = useState(false);
  const [showPollution, setShowPollution] = useState(false);

  const startAnalysis = async () => {

    if (new Date(startDate) > new Date(endDate)) {
      setError("Start date cannot be after End date");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {

      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          continent,
          country,
          city,
          start_date: startDate,
          end_date: endDate
        })
      });

      const data = await response.json();

      console.log("API RESULT:", data);

      if (!response.ok || !data.success) {
        setError(data.error || "Server error");
        return;
      }

      setResult(data);
      setGraphView(null);

    } catch {
      setError("Backend not responding");
    } finally {
      setLoading(false);
    }
  };

  if (stage === "title") {
    return (
      <div className="landing">
        <h1 className="title">🌍 SatelliteVision Pro</h1>
        <p className="subtitle">
          Real-time satellite based land cover & NDVI analysis
        </p>
        <button className="start-btn" onClick={() => setStage("analysis")}>
          Start Analysis
        </button>
      </div>
    );
  }

  return (

    <div className="app-container">

      <div className="analysis-card">

        <h2>Land Cover Analysis</h2>

        <div className="input-grid">

          <select value={continent} onChange={(e)=>{
            setContinent(e.target.value);
            setCountry("");
            setCity("");
          }}>
            <option value="">Select Continent</option>
            {Object.keys(DATA).map(c=>(
              <option key={c}>{c}</option>
            ))}
          </select>

          <select value={country} disabled={!continent} onChange={(e)=>{
            setCountry(e.target.value);
            setCity("");
          }}>
            <option value="">Select Country</option>
            {continent &&
              Object.keys(DATA[continent]).map(c=>(
                <option key={c}>{c}</option>
              ))}
          </select>

          <select value={city} disabled={!country} onChange={(e)=>setCity(e.target.value)}>
            <option value="">Select City</option>
            {continent && country &&
              DATA[continent][country].map(c=>(
                <option key={c}>{c}</option>
              ))}
          </select>

        </div>

        <div className="date-row">
          <input type="date" value={startDate} onChange={(e)=>setStartDate(e.target.value)} />
          <input type="date" value={endDate} onChange={(e)=>setEndDate(e.target.value)} />
        </div>

        <button className="analyze-btn" onClick={startAnalysis}>
          {loading ? "Analyzing..." : "Start Analysis"}
        </button>

        {error && <p className="error">{error}</p>}

      </div>

      {!loading && result && (

        <div className="results-section">

          <h3>Results</h3>

          <div className="image-card">
            <img src={result.analysis.satellite_image_url} alt="sat" />
          </div>

          <div className="chart-buttons">
            <button onClick={()=>setGraphView("bar")}>Bar Chart</button>
            <button onClick={()=>setGraphView("pie")}>Pie Chart</button>
          </div>

          {graphView === "bar" && (
            <LandCoverChart
              vegetation={result.analysis.land_cover.vegetation}
              urban={result.analysis.land_cover.urban}
              water={result.analysis.land_cover.water}
              bare={result.analysis.land_cover.bare_land}
            />
          )}

          {graphView === "pie" && (
            <LandCoverPie
              vegetation={result.analysis.land_cover.vegetation}
              urban={result.analysis.land_cover.urban}
              water={result.analysis.land_cover.water}
              bare={result.analysis.land_cover.bare_land}
            />
          )}

          <div className="info-card">

            <p><b>Location:</b> {result.location}</p>
            <p><b>NDVI:</b> {result.analysis.ndvi}</p>
            <p><b>Risk Level:</b> {result.analysis.risk}</p>

            <p style={{color:"red"}}>
              <b>ML Risk:</b> {result.analysis.ml_prediction}
            </p>

            <p><b>Confidence:</b> {result.analysis.ml_confidence}%</p>

            {/* ✅ ONLY THIS LINE ADDED */}
            <p><b>Model Accuracy:</b> {result.analysis.model_accuracy ?? 0}%</p>

            <div className="chart-buttons">
              <button onClick={()=>setShowLand(!showLand)}>📊 Land</button>
              <button onClick={()=>setShowRisk(!showRisk)}>⚠️ Risks</button>
              <button onClick={()=>setShowSuggest(!showSuggest)}>💡 Suggestions</button>
              <button onClick={()=>setShowFuture(!showFuture)}>🔮 Future</button>
              <button onClick={()=>setShowPollution(!showPollution)}>🌫 Pollution</button>
            </div>

            {showLand && (
              <>
                <h4>Land Cover</h4>
                <p>Vegetation: {result.analysis.land_cover.vegetation}</p>
                <p>Urban: {result.analysis.land_cover.urban}</p>
                <p>Water: {result.analysis.land_cover.water}</p>
                <p>Bare Land: {result.analysis.land_cover.bare_land}</p>
              </>
            )}

            {showRisk && (
              <>
                <h4>Detected Risks</h4>
                <ul>
                  {result.analysis.detected_risks?.map((r,i)=>(
                    <li key={i}>{r}</li>
                  ))}
                </ul>
              </>
            )}

            {showSuggest && (
              <>
                <h4>Suggestions</h4>
                <ul>
                  {result.analysis.dynamic_suggestions?.map((s,i)=>(
                    <li key={i}>{s}</li>
                  ))}
                </ul>
              </>
            )}

            {showFuture && (
              <>
                <h4>Future Prediction (10 Years)</h4>
                <p>Urban: {result.analysis.future_prediction?.future_urban ?? 0}%</p>
                <p>Vegetation: {result.analysis.future_prediction?.future_vegetation ?? 0}%</p>
                <p>Risk Score: {result.analysis.future_prediction?.future_risk_score ?? 0}</p>
                <p>Risk Level: {result.analysis.future_prediction?.future_risk_level ?? "N/A"}</p>
              </>
            )}

            {showPollution && (
              <>
                <h4>🛰️ Satellite Pollution (NO₂)</h4>
                <p><b>Level:</b> {result.analysis.air_pollution?.level}</p>
                <p><b>NO₂ Value:</b> {result.analysis.air_pollution?.no2_value}</p>

                <br />

                <h4>📊 AQI (OpenWeather - Approx)</h4>
                <p><b>AQI Index:</b> {result.analysis.real_time_aqi?.aqi}</p>
                <p><b>PM2.5:</b> {result.analysis.real_time_aqi?.pm2_5}</p>
                <p><b>PM10:</b> {result.analysis.real_time_aqi?.pm10}</p>

                <br />

                <h4 style={{color: "green"}}>🌍 Final AQI</h4>
                <p><b>AQI:</b> {result.analysis.real_aqi?.aqi}</p>
                <p><b>City:</b> {result.analysis.real_aqi?.city}</p>
              </>
            )}

          </div>

        </div>

      )}

    </div>
  );
}
