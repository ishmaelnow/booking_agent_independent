import { useState, useEffect } from "react";
import axios from "axios";

export default function BookRideStandalone() {
  const initialForm = {
    rider_name: "",
    pickup_location: "",
    dropoff_location: "",
    ride_time: "",
    phone_number: "",
  };

  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [timeoutWarning, setTimeoutWarning] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  useEffect(() => {
    let timer;
    if (loading) {
      timer = setTimeout(() => {
        setTimeoutWarning(true);
      }, 5000);
    }
    return () => clearTimeout(timer);
  }, [loading]);

  const formatPhone = (num) => {
    const digits = num.replace(/\D/g, "");
    if (digits.length === 10) {
      return `${digits.slice(0, 3)}-${digits.slice(3, 6)}-${digits.slice(6)}`;
    }
    return num;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setTimeoutWarning(false);
    setError("");
    setResult(null);

    try {
      const normalizedTime = form.ride_time
        ? new Date(form.ride_time).toISOString().slice(0, 16)
        : "";

      const payload = {
        rider_name: form.rider_name.trim(),
        pickup_location: form.pickup_location.trim(),
        dropoff_location: form.dropoff_location.trim(),
        ride_time: normalizedTime,
        phone_number: formatPhone(form.phone_number.trim()),
      };

      console.log("🚀 Submitting payload:", payload);

      const response = await axios.post(
        "https://booking-agent-api-f0d6.onrender.com/book/ride",
        payload,
        { headers: { "Content-Type": "application/json" } }
      );

      setResult(response.data);
      setForm(initialForm);
    } catch (err) {
      console.error("❌ Booking error:", err.response?.data || err.message);
      setError("🚨 Booking failed. Check your connection or try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "auto", padding: "2rem" }}>
      <h2>Book a Ride</h2>
      <form onSubmit={handleSubmit}>
        <input
          name="rider_name"
          type="text"
          placeholder="Passenger Name"
          value={form.rider_name}
          onChange={handleChange}
          required
        />
        <input
          name="pickup_location"
          type="text"
          placeholder="Pickup Location"
          value={form.pickup_location}
          onChange={handleChange}
          required
        />
        <input
          name="dropoff_location"
          type="text"
          placeholder="Dropoff Location"
          value={form.dropoff_location}
          onChange={handleChange}
          required
        />
        <input
          name="ride_time"
          type="datetime-local"
          value={form.ride_time}
          onChange={handleChange}
          required
        />
        <input
          name="phone_number"
          type="tel"
          placeholder="Phone Number"
          value={form.phone_number}
          onChange={handleChange}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Submitting…" : "Submit"}
        </button>
      </form>

      {timeoutWarning && !result && !error && (
        <p style={{ marginTop: "1rem" }}>⏳ Still working… hang tight.</p>
      )}

      {error && (
        <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>
      )}

      {result && (
        <div style={{ marginTop: "2rem" }}>
          <h3>Booking Summary</h3>
          <p><strong>Job ID:</strong> {result.job_id}</p>
          <p><strong>PIN:</strong> {result.pin}</p>
          <p><strong>Dispatch Info:</strong> {result.dispatch_info}</p>
          {result.driver_name && (
            <>
              <p><strong>Driver:</strong> {result.driver_name}</p>
              <p><strong>Vehicle:</strong> {result.vehicle}</p>
              <p><strong>Plate:</strong> {result.plate}</p>
              <p><strong>ETA:</strong> {result.eta_minutes} min</p>
            </>
          )}
          {result.estimated_miles && (
            <p><strong>Distance:</strong> {result.estimated_miles} mi</p>
          )}
          {result.fare_estimate && (
            <p><strong>Fare Estimate:</strong> ${result.fare_estimate}</p>
          )}
          {result.fare_explanation && (
            <p><strong>Fare Explanation:</strong> {result.fare_explanation}</p>
          )}
        </div>
      )}
    </div>
  );
}