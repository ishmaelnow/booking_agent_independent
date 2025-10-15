import { useState } from "react";
import { useNavigate } from "react-router-dom";
import IconHeader from "../components/IconHeader";
import Button from "../components/Button";
import { fetchDistance } from "../api/distance"; // ✅ Centralized axios call
import "../components/Button.css";
import "./DistanceTracker.css";

export default function DistanceTracker() {
  const navigate = useNavigate();

  const [pin, setPin] = useState("");
  const [distance, setDistance] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setDistance(null);

    if (!/^\d+$/.test(pin)) {
      setError("PIN must be numeric.");
      return;
    }

    try {
      setLoading(true);
      const response = await fetchDistance(Number(pin));
      console.log("Distance response:", response.data);

      const meters = response?.data?.distance_meters;
      if (typeof meters !== "number") {
        throw new Error("Malformed response: distance_meters missing.");
      }

      setDistance(meters);
    } catch (err) {
      console.error("Distance fetch error:", err);
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        "Unexpected error occurred.";
      setError(msg);
    } finally {
      setLoading(false);
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
            type="text"
            inputMode="numeric"
            pattern="\d*"
            placeholder="Enter Access PIN"
            value={pin}
            onChange={(e) => setPin(e.target.value.trim())}
            required
          />

          <Button type="submit" variant="success" disabled={loading}>
            {loading ? "Checking…" : "✅ Check Distance"}
          </Button>
        </form>

        {distance !== null && (
          <div className="result" style={{ marginTop: 12 }}>
            <h3>Distance Result</h3>
            <p>
              🛣️ <strong>{distance.toFixed(2)} meters</strong>
            </p>
          </div>
        )}

        {error && (
          <div className="error" role="alert" style={{ marginTop: 12 }}>
            ⚠️ {error}
          </div>
        )}
      </div>
    </div>
  );
}