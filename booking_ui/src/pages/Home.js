import { useNavigate } from "react-router-dom";
import "./Home.css";
import Button from "../components/Button";

// Modular HomeDetails components (re-exported from components/index.js)
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
        <Button onClick={() => navigate("/feedback")} variant="secondary">
  🛠️ Submit Feedback
        </Button>
      </main>

      {/* Fleet & Coverage Images */}
      <section className="fleet-showcase">
        <h2>🚗 Our Fleet & Coverage</h2>

        <div className="fleet-card">
          <img className="fleet-image" src="/images/carsline.png" alt="Lineup of Cars" />
        </div>

        <div className="fleet-card">
          <img className="fleet-image" src="/images/dfwroads.png" alt="DFW Roadways" />
        </div>
      </section>

      {/* Extended HomeDetails Sections */}
      <section className="home-section">
        <HeroSection />
      </section>

      <section className="home-section">
        <BookingOptions />
      </section>

      <section className="home-section">
        <FleetGallery />
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