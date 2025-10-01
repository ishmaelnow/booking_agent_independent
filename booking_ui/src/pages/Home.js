import { Link } from "react-router-dom";
import "./Home.css";

export default function Home() {
  return (
    <div className="home-wrapper">
      <header className="home-header">
        <h1>🚕 Fairfare Portal</h1>
        <p>Plan your ride with ease</p>
      </header>

      <main className="home-actions">
        <Link to="/book" className="home-button book">
          🚗 Book a Ride
        </Link>
        <Link to="/fare-preview" className="home-button fare">
          💰 Fare Estimate
        </Link>
      </main>
    </div>
  );
}