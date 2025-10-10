import React, { useState } from "react";
import "./FeedbackForm.css";
import Button from "../components/Button";
import { useNavigate } from "react-router-dom";
import { submitFeedback } from "../api/feedback"; // ✅ Modular API import

const FeedbackForm = () => {
  const [pin, setPin] = useState("");
  const [rating, setRating] = useState(5);
  const [comments, setComments] = useState("");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const navigate = useNavigate();

  const handleSubmit = async () => {
    setError(null);
    setResponse(null);

    try {
      const res = await submitFeedback(pin, rating, comments);
      setResponse(res.data.confirmation);
    } catch (err) {
      setError(err.response?.data?.detail || "Unexpected error occurred.");
    }
  };

  return (
    <div className="feedback-form">
      <h2>📝 Submit Ride Feedback</h2>

      <input
        type="number"
        placeholder="Enter your PIN"
        value={pin}
        onChange={(e) => setPin(e.target.value)}
      />

      <select value={rating} onChange={(e) => setRating(parseInt(e.target.value))}>
        {[5, 4, 3, 2, 1].map((r) => (
          <option key={r} value={r}>{r} Stars</option>
        ))}
      </select>

      <textarea
        placeholder="Write your feedback..."
        value={comments}
        onChange={(e) => setComments(e.target.value)}
      />

      <button onClick={handleSubmit}>Submit Feedback</button>

      {response && <p className="success">{response}</p>}
      {error && <p className="error">❌ {error}</p>}

      <Button label="← Back to Home" onClick={() => navigate("/")} />
    </div>
  );
};

export default FeedbackForm;