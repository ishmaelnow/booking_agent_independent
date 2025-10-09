import React from "react";
import { Link } from "react-router-dom";

export default function BookingOptions() {
  return (
    <section className="booking-options">
      <h2>How to Book a Ride</h2>
      <div className="booking-grid">
        <div className="booking-item">
          <h3>📞 Call by Phone</h3>
          <p><strong>Dallas Fort Worth Metroplex:</strong></p>
          <p>📞 469-835-7520</p>
          <p>📞 469-268-8239</p>
        </div>
        <div className="booking-item">
          <h3>🚖 Hail on the Street</h3>
          <p>Just like a taxi, hop in when you see us!</p>
        </div>
        <div className="booking-item">
          <h3>🌐 Book Online</h3>
          <p>No smartphone needed, book directly on our website.</p>
        </div>
      </div>
    </section>
  );
}