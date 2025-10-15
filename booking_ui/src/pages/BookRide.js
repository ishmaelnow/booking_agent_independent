import { useState } from "react";
import { useNavigate } from "react-router-dom";
import IconHeader from "../components/IconHeader";
import Button from "../components/Button";
import { bookRide } from "../api/booking";
import "../components/Button.css";
import "./BookRide.css";

export default function BookRide() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    rider_name: "",
    pickup_location: "",
    dropoff_location: "",
    ride_time: "now",            // default that the backend understands
    phone_number: "",
  });

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null); // backend returns a flat object

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError("");
    setResult(null);

    // Build payload: keep "now" unless user chose a datetime
    const payload = {
      ...form,
      ride_time: form.ride_time && form.ride_time !== "" ? form.ride_time : "now",
    };

    try {
      const { data } = await bookRide(payload);
      setResult(data); // data is { job_id, pin, dispatch_info, fare_estimate, ... }
      // Do not navigate automatically; user can choose to track.
    } catch (err) {
      console.error("Submission error:", err);
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        "Something went wrong while booking your ride.";
      setError(msg);
    } finally {
      setSubmitting(false);
    }
  };

  const handleTrackRide = () => {
    if (result?.pin) {
      navigate(`/live?pin=${encodeURIComponent(result.pin)}`);
    }
  };

  return (
    <div className="page-wrapper">
      <div className="form-container">
        <Button variant="primary" onClick={() => navigate("/")}>
          🏠 Back to Home
        </Button>

        <IconHeader title="Book a Ride" />

        <form onSubmit={handleSubmit} className="booking-form">
          <input
            type="text"
            name="rider_name"
            value={form.rider_name}
            onChange={handleChange}
            placeholder="Passenger Name"
            required
          />

          <input
            type="text"
            name="pickup_location"
            value={form.pickup_location}
            onChange={handleChange}
            placeholder="Pickup Location"
            required
          />

          <input
            type="text"
            name="dropoff_location"
            value={form.dropoff_location}
            onChange={handleChange}
            placeholder="Dropoff Location"
            required
          />

          {/* If you want to let the user choose a time, leave this input.
              Otherwise, keep "now" as the default and hide this input. */}
          <input
            type="text"
            name="ride_time"
            value={form.ride_time}
            onChange={handleChange}
            placeholder='Ride Time (e.g., "now" or 2025-10-13T08:30)'
          />

          <input
            type="tel"
            name="phone_number"
            value={form.phone_number}
            onChange={handleChange}
            placeholder="Phone Number"
            required
          />

          <Button type="submit" variant="success" disabled={submitting}>
            {submitting ? "Submitting…" : "✅ Submit"}
          </Button>
        </form>

        {error && (
          <div className="error-box" role="alert" style={{ marginTop: 12 }}>
            {error}
          </div>
        )}

        {result && (
          <div className="fare-summary" style={{ marginTop: 16 }}>
            <h3>Ride Summary</h3>

            {/* Core ride + dispatch info */}
            {result.job_id && (
              <p>
                <strong>Job ID:</strong> {result.job_id}
              </p>
            )}

            {result.dispatch_info && (
              <p style={{ whiteSpace: "pre-line" }}>
                <strong>Dispatch:</strong> {result.dispatch_info}
              </p>
            )}

            {(result.driver_name || result.vehicle || result.plate) && (
              <p>
                <strong>Driver:</strong>{" "}
                {[
                  result.driver_name,
                  result.vehicle && `(${result.vehicle}`,
                  result.plate && `${result.vehicle ? "," : "("} ${result.plate}`,
                ]
                  .filter(Boolean)
                  .join(" ")
                  .replace(/\s+\(/, " (")}
                {result.vehicle || result.plate ? ")" : ""}
              </p>
            )}

            {typeof result.eta_minutes === "number" && (
              <p>
                <strong>ETA:</strong> {result.eta_minutes} minutes
              </p>
            )}

            {/* Fare details */}
            {typeof result.estimated_miles !== "undefined" && (
              <p>
                <strong>Miles:</strong> {result.estimated_miles} mi
              </p>
            )}

            {typeof result.fare_estimate !== "undefined" && (
              <p>
                <strong>Estimated Fare:</strong> ${result.fare_estimate}
              </p>
            )}

            {result.fare_explanation && (
              <p>
                <strong>Note:</strong> {result.fare_explanation}
              </p>
            )}

            {/* Tracking PIN */}
            {result.pin && (
              <>
                <p>
                  <strong>Access PIN:</strong> 🔒 {result.pin}
                </p>
                <Button variant="primary" onClick={handleTrackRide}>
                  🚗 Track My Ride
                </Button>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
