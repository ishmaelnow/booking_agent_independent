import "./FeedbackForm.css";
import Button from "../components/Button";
import "../components/Button.css";
import { useNavigate } from "react-router-dom";

export default function FeedbackForm() {
  const navigate = useNavigate(); // ✅ Define navigate properly

  return (
    <div className="feedback-wrapper">
      <div className="form-container">
        <Button variant="primary" onClick={() => navigate("/")}>
          🏠 Back to Home
        </Button>
      </div>

      <h1>🛠️ Submit Feedback</h1>
      <p>We value your input. Let us know how we can improve.</p>

      <form className="feedback-form">
        <label>
          Ride ID (optional):
          <input type="text" name="rideId" />
        </label>

        <label>
          Rating:
          <select name="rating">
            <option value="">Select</option>
            <option value="5">⭐️⭐️⭐️⭐️⭐️</option>
            <option value="4">⭐️⭐️⭐️⭐️</option>
            <option value="3">⭐️⭐️⭐️</option>
            <option value="2">⭐️⭐️</option>
            <option value="1">⭐️</option>
          </select>
        </label>

        <label>
          Comments:
          <textarea
            name="comments"
            rows="5"
            placeholder="Tell us what went well or what could be better..."
          />
        </label>

        <button type="submit">Submit Feedback</button>
      </form>
    </div>
  );
}