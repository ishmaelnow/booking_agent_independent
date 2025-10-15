import { useState } from "react";
import axios from "axios";

const BASE = process.env.REACT_APP_API_URL;

export default function TestBackendPing() {
  const [response, setResponse] = useState(null);
  const [error, setError] = useState("");

  const testPayload = {
    rider_name: "Ping Tester",
    pickup_location: "Dallas",
    dropoff_location: "Plano",
    ride_time: new Date().toISOString().slice(0, 16),
    phone_number: "555-9999",
  };

  const ping = async () => {
    try {
      console.log("Sending test payload:", testPayload);
      const res = await axios.post(`${BASE}/book/ride`, testPayload, {
        headers: { "Content-Type": "application/json" },
      });
      console.log("✅ Backend response:", res.data);
      setResponse(res.data);
    } catch (err) {
      console.error("❌ Backend ping failed:", err);
      setError("Could not reach backend. Check URL, CORS, or route registration.");
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>🔍 Backend Ping Test</h2>
      <button onClick={ping}>Send Test Booking</button>

      {response && (
        <div style={{ marginTop: "1rem", background: "#e0ffe0", padding: "1rem" }}>
          <strong>✅ Success:</strong>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}

      {error && (
        <div style={{ marginTop: "1rem", background: "#ffe0e0", padding: "1rem" }}>
          <strong>{error}</strong>
        </div>
      )}
    </div>
  );
}