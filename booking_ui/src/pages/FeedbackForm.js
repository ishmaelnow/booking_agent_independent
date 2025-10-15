import React, { useState } from "react";
import "./FeedbackForm.css";
import Button from "../components/Button";
import { useNavigate } from "react-router-dom";
import api from "../api/booking"; // ✅ Centralized axios instance

const FeedbackForm = () => {
  const navigate = useNavigate();

  const [pin, setPin] = useState("");
  const [rating, setRating] = useState(5);
  const [comments, setComments] = useState("");

  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const submitFeedback = async () => {
    setError(null);
    setResponse(null);

    if (!/^\d+$/.test(pin)) {
      setError("PIN must be numeric.");
      return;
    }

    try {
      setLoading(true);

      const payload = {
        pin: Number(pin),
        feedback_rating: Number(rating),
        feedback_comments: comments?.trim() ?? "",
      };

      const res = await api.post("/book/feedback", payload);
      const confirmation = res?.data?.confirmation || "Thanks! Your feedback was recorded.";

      setResponse(confirmation);
      setComments("");
      setPin("");
      setRating(5);
    } catch (err) {
      console.error("Feedback error:", err);
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        "Unexpected error submitting feedback.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="feedback-form">
      <h2>📝 Submit Ride Feedback</h2>

      <input
        type="text"
        inputMode="numeric"
        pattern="\d*"
        placeholder="Enter your PIN"
        value={pin}
        onChange={(e) => setPin(e.target.value.trim())}
      />

      <select
        value={rating}
        onChange={(e) => setRating(parseInt(e.target.value, 10))}
      >
        {[5, 4, 3, 2, 1].map((r) => (
          <option key={r} value={r}>
            {r} Stars
          </option>
        ))}
      </select>

      <textarea
        placeholder="Write your feedback..."
        value={comments}
        onChange={(e) => setComments(e.target.value)}
      />

      <button onClick={submitFeedback} disabled={loading}>
        {loading ? "Submitting…" : "Submit Feedback"}
      </button>

      {response && <p className="success">✅ {response}</p>}
      {error && <p className="error">❌ {error}</p>}

      <Button label="← Back to Home" onClick={() => navigate("/")} />
    </div>
  );
};

export default FeedbackForm;