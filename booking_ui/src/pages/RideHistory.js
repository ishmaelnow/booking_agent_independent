import { useState, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { fetchRideHistory } from "../api/history"; // ✅ Modular API import
import IconHeader from "../components/IconHeader";
import Button from "../components/Button";
import "./RideHistory.css";

export default function RideHistory() {
  const navigate = useNavigate();

  const [pin, setPin] = useState("");
  const [rides, setRides] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const normalizeRide = (r) => {
    const rideTime = r.ride_time || r.timestamp || r.created_at || r.createdAt || "";
    const pickup = r.pickup_location || r.pickup || (r.state && r.state.pickup_location) || "";
    const dropoff = r.dropoff_location || r.dropoff || (r.state && r.state.dropoff_location) || "";
    const fareRaw = r.fare_estimate || r.fare || (r.state && r.state.fare_estimate) || "";

    let fare = fareRaw;
    const n = Number(fareRaw);
    if (!Number.isNaN(n) && Number.isFinite(n)) {
      fare = n.toFixed(2);
    }

    return {
      id: r.id ?? `${rideTime}-${pickup}-${dropoff}-${fare}`,
      ride_time: String(rideTime),
      pickup,
      dropoff,
      fare,
    };
  };

  const displayRides = useMemo(() => rides.map(normalizeRide), [rides]);

  const fetchHistory = async () => {
    const trimmedPin = String(pin).trim();
    if (!trimmedPin) {
      setError("Please enter your PIN.");
      setRides([]);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetchRideHistory(trimmedPin);
      const list = Array.isArray(response?.data?.bookings) ? response.data.bookings : [];
      setRides(list);
      if (list.length === 0) {
        setError("No rides found for this PIN.");
      }
    } catch (err) {
      const status = err?.response?.status;
      const detail = err?.response?.data?.detail;

      if (status === 404) {
        setRides([]);
        setError(detail || "No rides found for this PIN.");
      } else if (status === 400) {
        setRides([]);
        setError(detail || "Missing or invalid PIN.");
      } else if (err?.message?.includes("Network Error")) {
        setRides([]);
        setError("Network error: could not reach the server.");
      } else {
        setRides([]);
        setError(detail || "Failed to fetch ride history.");
      }

      console.error("Error fetching history:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") fetchHistory();
  };

  return (
    <div className="page-wrapper">
      <div className="form-container">
        <Button variant="secondary" onClick={() => navigate("/")}>
          ← Back to Home
        </Button>

        <IconHeader title="Ride History" />

        <input
          type="password"
          value={pin}
          onChange={(e) => setPin(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Enter your PIN"
          aria-label="PIN"
          autoComplete="one-time-code"
        />

        <Button onClick={fetchHistory} variant="primary" disabled={loading}>
          {loading ? "Fetching..." : "Fetch History"}
        </Button>

        {error && (
          <div className="alert error" role="alert" style={{ marginTop: 12 }}>
            {error}
          </div>
        )}

        {displayRides.length > 0 && !loading && (
          <div className="history-list">
            {displayRides.map((ride) => (
              <div key={ride.id} className="ride-card">
                <p><strong>Date:</strong> {ride.ride_time || "—"}</p>
                <p><strong>From:</strong> {ride.pickup || "—"}</p>
                <p><strong>To:</strong> {ride.dropoff || "—"}</p>
                <p><strong>Fare:</strong> {ride.fare !== "" ? `$${ride.fare}` : "—"}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}