import React, { useState } from "react";
import './FeedbackForm.css'; // ✅ Adjust path if needed

const FeedbackForm = () => {
  const [pin, setPin] = useState("");
  const [rating, setRating] = useState(5);
  const [comments, setComments] = useState("");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const submitFeedback = async () => {
    setError(null);
    setResponse(null);

    try {
      const res = await fetch("http://localhost:8000/book/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          pin: parseInt(pin),
          feedback_rating: rating,
          feedback_comments: comments,
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Unknown error");

      setResponse(data.confirmation);
    } catch (err) {
      setError(err.message);
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

      <button onClick={submitFeedback}>Submit Feedback</button>

      {response && <p className="success">{response}</p>}
      {error && <p className="error">❌ {error}</p>}
    </div>
  );
};

export default FeedbackForm;