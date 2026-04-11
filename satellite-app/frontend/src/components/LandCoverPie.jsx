import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

function LandCoverPie({ vegetation, urban, water, bare }) {

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
        ],
        borderWidth: 1
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false
  };

  return (
    <div style={{ width: "100%", maxWidth: "500px", height: "300px", margin: "20px auto" }}>
      <h3>Land Cover Distribution</h3>
      <Pie data={data} options={options} />
    </div>
  );
}

export default LandCoverPie;