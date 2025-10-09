import { useState } from "react";
import { useNavigate } from "react-router-dom";
import IconHeader from "../components/IconHeader";
import Button from "../components/Button";
import { fetchDistance } from "../api/distance";
import "../components/Button.css";
import "./DistanceTracker.css"; // Optional: create for styling

export default function DistanceTracker() {
  const navigate = useNavigate();
  const [pin, setPin] = useState("");
  const [distance, setDistance] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setDistance(null);

    try {
      const response = await fetchDistance(parseInt(pin));
      setDistance(response.data.distance_meters);
    } catch (err) {
      setError(err.response?.data?.detail || "Unexpected error occurred.");
    }
  };

  return (
    <div className="page-wrapper">
      <div className="form-container">
        <Button variant="primary" onClick={() => navigate("/")}>
          🏠 Back to Home
        </Button>

        <IconHeader title="📍 Distance Tracker" />

        <form onSubmit={handleSubmit} className="distance-form">
          <input
            type="number"
            placeholder="Enter Access PIN"
            value={pin}
            onChange={(e) => setPin(e.target.value)}
            required
          />
          <Button type="submit" variant="success">
            ✅ Check Distance
          </Button>
        </form>

        {distance !== null && (
          <div className="result">
            <h3>Distance Result</h3>
            <p>🛣️ <strong>{distance.toFixed(2)} meters</strong></p>
          </div>
        )}

        {error && (
          <div className="error">
            <p>⚠️ {error}</p>
          </div>
        )}
      </div>
    </div>
  );
}