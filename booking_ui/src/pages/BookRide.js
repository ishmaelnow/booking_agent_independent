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
    ride_time: "",
    phone_number: "",
  });

  const [bookingResult, setBookingResult] = useState(null); // ✅ Added

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await bookRide(form);
      setBookingResult(response.data); // ✅ Store full response
      console.log("Booking confirmed:", response.data);
    } catch (error) {
      console.error("Submission error:", error);
    }
  };

  return (
    <div className="page-wrapper">
      <div className="form-container">
        <Button variant="secondary" onClick={() => navigate("/")}>
          ← Back to Home
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
            name="pickup_location" // ✅ corrected
            value={form.pickup_location} // ✅ corrected
            onChange={handleChange}
            placeholder="Pickup Location"
            required
          />
          <input
            type="text"
            name="dropoff_location" // ✅ corrected
            value={form.dropoff_location} // ✅ corrected
            onChange={handleChange}
            placeholder="Dropoff Location"
            required
          />
          <input
            type="datetime-local"
            name="ride_time"
            value={form.ride_time}
            onChange={handleChange}
            required
          />
          <input
            type="tel"
            name="phone_number"
            value={form.phone_number}
            onChange={handleChange}
            placeholder="Phone Number"
            required
          />

          <Button type="submit" variant="primary">
            Submit
          </Button>
        </form>

        {bookingResult && (
          <div className="fare-summary">
            <h3>Fare Estimate</h3>
            <p><strong>From:</strong> {bookingResult.booking.pickup_location}</p>
            <p><strong>To:</strong> {bookingResult.booking.dropoff_location}</p>
            <p><strong>Miles:</strong> {bookingResult.booking.estimated_miles} mi</p>
            <p><strong>Estimated Fare:</strong> ${bookingResult.booking.fare_estimate}</p>
            <p><strong>Explanation:</strong> {bookingResult.booking.fare_explanation}</p>
          </div>
        )}
      </div>
    </div>
  );
}