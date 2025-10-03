import React from "react";
import { Link } from "react-router-dom";

export default function HeroSection() {
  return (
    <section className="hero">
      <h1>Welcome to FairFare Transportation</h1>
      <p>
        We offer professional and dependable transportation services, including traditional taxi rides, shared rides, and group corporate transportation.
      </p>
      <p>Contact us today to explore our full range of services.</p>
      <div className="hero-media">
        <img src="/images/dfw-areas-hero.png" alt="DFW skyline and roads" />
      </div>
      <h2>Ready to Ride?</h2>
      <Link to="/register" className="btn btn-primary">Register to Book</Link>
    </section>
  );
}