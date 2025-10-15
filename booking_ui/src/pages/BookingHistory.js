import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import IconHeader from "../components/IconHeader";
import Button from "../components/Button";
import api from "../api/booking"; // ✅ Centralized axios instance
import "./BookingHistory.css";

export default function BookingHistory() {
  const navigate = useNavigate();
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchBookings = async () => {
    setLoading(true);
    setError("");
    setBookings([]);

    try {
      const res = await api.get("/bookings/view", {
        params: { limit: 20, offset: 0 },
      });

      const items = Array.isArray(res?.data?.items) ? res.data.items : [];
      setBookings(items);

      if (items.length === 0) {
        setError("No bookings found.");
      }
    } catch (err) {
      console.error("Booking history error:", err);
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        "Failed to fetch booking history.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBookings();
  }, []);

  return (
    <div className="page-wrapper">
      <div className="form-container">
        <Button variant="primary" onClick={() => navigate("/")}>
          🏠 Back to Home
        </Button>

        <IconHeader title="📦 Booking History" />

        {loading && <p>Loading bookings…</p>}

        {error && (
          <div className="error" role="alert" style={{ marginTop: 12 }}>
            ⚠️ {error}
          </div>
        )}

        {!loading && bookings.length > 0 && (
          <div className="history-list">
            {bookings.map((b, i) => (
              <div key={b.job_id || i} className="booking-card">
                <p><strong>Job ID:</strong> {b.job_id}</p>
                <p><strong>Pickup:</strong> {b.pickup_location || "—"}</p>
                <p><strong>Dropoff:</strong> {b.dropoff_location || "—"}</p>
                <p><strong>Fare:</strong> {b.fare_estimate ? `$${b.fare_estimate}` : "—"}</p>
                <p><strong>Status:</strong> {b.claimed ? "Claimed" : "Open"}</p>
                {b.created_at && (
                  <p><strong>Time:</strong> {new Date(b.created_at).toLocaleString()}</p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}