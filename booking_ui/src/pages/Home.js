import {  useNavigate } from "react-router-dom";
import "./Home.css";
import Button from "../components/Button";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-wrapper">
      <header className="home-header">
        <h1>🚕 Fairfare Portal</h1>
        <p>Plan your ride with ease</p>
      </header>

      <main className="home-actions">
        <Button onClick={() => navigate("/book")} variant="primary">
          🚗 Book a Ride
        </Button>
        <Button onClick={() => navigate("/history")} variant="secondary">
          📜 View Ride History
        </Button>
        <Button onClick={() => navigate("/fare-preview")} variant="secondary">
          💰 Fare Estimate
        </Button>
      </main>
    </div>
  );
}