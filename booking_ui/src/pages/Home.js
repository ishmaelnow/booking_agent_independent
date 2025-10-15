import { useNavigate } from "react-router-dom";
import "./Home.css";
import Button from "../components/Button";

// Modular HomeDetails components
import {
  HeroSection,
  BookingOptions,
  FleetGallery,
  FeatureList,
  RateTable,
  CompanyOverview,
  PolicySection,
  AccessibilityInfo,
} from "../components";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-wrapper">
      <header className="home-header">
        <h1>🚕 Fairfare Portal</h1>
        <p>Plan your ride with ease</p>
      </header>

      <section className="hero-section">
        <HeroSection />
      </section>

      <main className="home-actions">
        {/* 🧍 Rider Actions */}
        <Button onClick={() => navigate("/book")} variant="primary">
          🚗 Book a Ride
        </Button>
        <Button onClick={() => navigate("/history")} variant="secondary">
          📜 View Ride History
        </Button>
        <Button onClick={() => navigate("/fare-preview")} variant="secondary">
          💰 Fare Estimate
        </Button>
        <Button onClick={() => navigate("/feedback")} variant="secondary">
          🛠️ Submit Feedback
        </Button>
        <Button onClick={() => navigate("/stand-alone")} variant="secondary">
          🚗 Standalone Booking
        </Button>

        {/* 📡 Tracking Tools */}
        <Button onClick={() => navigate("/distance")} variant="info">
          📍 Track Distance
        </Button>
        <Button onClick={() => navigate("/live")} variant="info">
          🛰️ View Live Tracker
        </Button>

        {/* 🧪 Admin & Debug */}
        <Button onClick={() => navigate("/test-ping")} variant="warning">
          🧪 Backend Ping Test
        </Button>
        <Button onClick={() => navigate("/jobs")} variant="warning">
          🧾 View Job Queue
        </Button>
        <Button onClick={() => navigate("/bookings")} variant="warning">
          📦 Booking History
        </Button>
      </main>

      <section className="fleet-showcase">
        <h2>🚗 Our Fleet & Coverage</h2>
        <div className="fleet-card">
          <FleetGallery />
        </div>
      </section>

      <section className="home-section">
        <BookingOptions />
      </section>

      <section className="dfw-area">
        <img className="fleet-image" src="/images/dfw-areas-hero.png" alt="DFW Sky Line" />
      </section>

      <section className="home-section">
        <FeatureList />
      </section>

      <section className="home-section">
        <RateTable />
      </section>

      <section className="home-section">
        <CompanyOverview />
      </section>

      <section className="home-section">
        <PolicySection />
      </section>

      <section className="home-section">
        <AccessibilityInfo />
      </section>
      
    </div>
  );
}