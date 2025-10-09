// src/components/Button.js
import React from "react";
import "./Button.css";

export default function Button({ children, onClick, variant = "primary", type = "button" }) {
  return (
    <button type={type} className={`btn ${variant}`} onClick={onClick}>
      {children}
    </button>
  );
}