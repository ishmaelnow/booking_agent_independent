// src/components/HomeDetails/HeroSection.js
import React from "react";

export default function HeroSection() {
  return (
    <section className="hero-section">
  <div className="hero-text">
    <h1 className="hero-title">Welcome to FairFare Transportation</h1>
    <p>We offer professional and dependable transportation services, including traditional taxi rides, shared rides, and group corporate transportation.</p>
    <p>Contact us today to explore our full range of services.</p>
  </div>

  <div className="hero-media">
    <img src="images/dfwroads.png" alt="DFW skyline and roads" />
  </div>

  <h2>Ready to Ride?</h2>
</section>
  );
}
