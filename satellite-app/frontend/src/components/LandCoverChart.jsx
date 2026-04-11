import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

function LandCoverChart({ vegetation, urban, water, bare }) {

  const data = {
    labels: ["Vegetation", "Urban", "Water", "Bare Land"],
    datasets: [
      {
        label: "Land Cover %",
        data: [vegetation, urban, water, bare],
        backgroundColor: [
          "#2ecc71",
          "#e74c3c",
          "#3498db",
          "#f1c40f"
        ]
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false
  };

  return (
    <div style={{ width: "100%", maxWidth: "500px", height: "300px", margin: "20px auto" }}>
      <h3>Land Cover Analysis</h3>
      <Bar data={data} options={options} />
    </div>
  );
}

export default LandCoverChart;