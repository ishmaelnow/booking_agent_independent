// src/api/feedback.js
import { api } from "./client";

export const submitFeedback = (pin, rating, comments) => {
  return api.post("/book/feedback", {
    pin: parseInt(pin),
    feedback_rating: rating,
    feedback_comments: comments,
  });
};