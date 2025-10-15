import { useState, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import IconHeader from "../components/IconHeader";
import Button from "../components/Button";
import api from "../api/booking"; // ✅ Centralized axios instance
import "./RideHistory.css";

export default function RideHistory() {
  const navigate = useNavigate();
  const [rides, setRides] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const normalizeRide = (r) => {
    const pickup = r.pickup_location ?? r.pickup ?? "";
    const dropoff = r.dropoff_location ?? r.dropoff ?? "";
    const fareRaw = r.fare_estimate ?? r.fare ?? "";
    const fareNum = Number(fareRaw);
    const fare =
      Number.isFinite(fareNum) && !Number.isNaN(fareNum)
        ? fareNum.toFixed(2)
        : String(fareRaw ?? "");

    return {
      id: r.id ?? `${pickup}-${dropoff}-${fare}`,
      pickup,
      dropoff,
      fare,
      claimed: Boolean(r.claimed),
    };
  };

  const displayRides = useMemo(() => rides.map(normalizeRide), [rides]);

  const fetchHistory = async () => {
    setLoading(true);
    setError(null);
    setRides([]);

    try {
      const res = await api.get("/book/history", {
        params: { limit: 20, offset: 0 },
      });

      const items = Array.isArray(res?.data?.items) ? res.data.items : [];
      setRides(items);

      if (items.length === 0) {
        setError("No rides found yet.");
      }
    } catch (err) {
      console.error("Error fetching ride history:", err);
      const detail = err?.response?.data?.detail;
      setError(detail || "Failed to fetch ride history.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-wrapper">
      <div className="form-container">
        <Button variant="secondary" onClick={() => navigate("/")}>
          ← Back to Home
        </Button>

        <IconHeader title="Ride History" />

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
                <p><strong>From:</strong> {ride.pickup || "—"}</p>
                <p><strong>To:</strong> {ride.dropoff || "—"}</p>
                <p><strong>Fare:</strong> {ride.fare !== "" ? `$${ride.fare}` : "—"}</p>
                <p><strong>Status:</strong> {ride.claimed ? "Claimed" : "Open"}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}