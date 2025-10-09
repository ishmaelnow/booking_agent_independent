// src/pages/Home.js
import React from "react";
import { Link } from "react-router-dom";
// import MapContainer from "../components/MapContainer"; // removed
import "./Test.css";

/* Export at the top so other files can import this component */
export default function Test() {
  const features = [
    { title: "Quick and Easy Booking", description: "Book your ride in just a few clicks." },
    { title: "Affordable Pricing", description: "Get the best rates for your journeys." },
    { title: "Safe and Reliable", description: "All our drivers are verified and professional." },
    { title: "24/7 Service", description: "Available anytime you need a ride in the Dallas/Fort Worth area." },
    { title: "Wheelchair Accessible", description: "Wheelchair-accessible vehicles are available upon request." },
  ];

  const taxiRates = [
    { category: "Initial Meter Drop", price: "$3.00" },
    { category: "Per 1/4 Mile", price: "$0.70" },
    { category: "Traffic Delay / Waiting Time (Per Min)", price: "$0.40" },
    { category: "Extra Passenger", price: "$2.00" },
    { category: "Minimum Charge (Love Field Airport)", price: "$10.00" },
    { category: "Love Field Trip Fee", price: "$2.00" },
    { category: "Flat Rate (Love Field ↔ Dallas Central Business District)", price: "$26.00" },
    { category: "Flat Rate (DFW Airport ↔ Dallas Central Business District)", price: "$55.00" },
    { category: "DFW Airport Exit Fee", price: "$5.00" },
    { category: "DFW Airport Drop-off Fee", price: "$4.00" },
    { category: "Minimum Fare (DFW Airport to Off-Airport)", price: "$27.00" },
  ];

  return (
    <div className="home-container">
      {/* Hero Section */}
      <section className="hero">
        <h1>Welcome to FairFare Transportation</h1>
        <p>
          We offer professional and dependable transportation services, including traditional taxi rides, shared rides, and group corporate transportation.
        </p>
        <p>Contact us today to explore our full range of services.</p>

        {/* Hero media (photo replaces map) */}
        <div className="hero-media">
          <img
            src="/images/dfw-areas-hero.png"
            alt="DFW AREAS — Dallas–Fort Worth skyline and roads"
          />
        </div>

        <h2>Ready to Ride?</h2>
        <div className="buttons">
          <Link to="/register" className="btn btn-primary">Register to Book</Link>
        </div>
      </section>

      {/* Booking Methods */}
      <section className="booking-options">
        <h2>How to Book a Ride</h2>
        <div className="booking-grid">
          <div className="booking-item">
            <h3>📞 Call by Phone</h3>
            <p>No smartphone? No problem! Call us at:</p>
            <p><strong>Dallas Fort Worth Metroplex:</strong></p>
            <p>📞 469-835-7520</p>
            <p>📞 469-268-8239</p>
          </div>
          <div className="booking-item">
            <h3>🚖 Hail on the Street</h3>
            <p>Just like a taxi, hop in when you see us!</p>
          </div>
          <div className="booking-item">
            <h3>🌐 Book Online</h3>
            <p>No smartphone needed, book directly on our website.</p>
            <Link to="/book" className="btn btn-secondary">Book Now</Link>
          </div>
        </div>
      </section>

      {/* Fleet Images Section */}
      <section className="fleet">
        <div className="fleet-grid">
          <div className="fleet-item">
            <img src="/images/left-image.png" alt="Fleet Car 1" className="fleet-image" />
          </div>
          <div className="fleet-item">
            <img src="/images/right-image.png" alt="Fleet Car 2" className="fleet-image" />
          </div>
          <div className="fleet-item">
            <img src="/images/van.png" alt="Fleet Van" className="fleet-image" />
          </div>
          <div className="fleet-item">
            <img src="/images/pavan.png" alt="Passenger Van" className="fleet-image" />
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <h2>Why Choose Us?</h2>
        <ul>
          {features.map((feature) => (
            <li key={feature.title}>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </li>
          ))}
        </ul>
      </section>

      {/* Taxi Rates */}
      <section className="rates">
        <h2>Taxi Cab Rates</h2>
        <table className="rate-table">
          <thead>
            <tr>
              <th>Service</th>
              <th>Rate</th>
            </tr>
          </thead>
          <tbody>
            {taxiRates.map(({ category, price }) => (
              <tr key={category}>
                <td>{category}</td>
                <td>{price}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      {/* Company Overview */}
      <section className="company-overview">
        <h2>About Fair Fare Transportation</h2>
        <p>
          FairFare Transportation is a professional, reliable, and dependable taxi service.
          We offer door-to-door transportation 24/7 across the Dallas/Fort Worth Metroplex.
          Whether you need a ride to <strong>DFW International Airport, Love Field Airport, or anywhere in town</strong>,
          we’ve got you covered.
        </p>
        <p>
          Our drivers are <strong>bonded and professional</strong>, monitored by field supervisors to ensure
          <strong> safe and quality service</strong>. Whether it's an airport trip, corporate travel, or a special event,
          we guarantee <strong>on-time service</strong> and <strong>affordable rates</strong>.
        </p>
      </section>

      {/* Company Policies */}
      <section className="company-policies">
        <h2>Our Commitment to Safety & Service</h2>

        <div className="policy-item">
          <h3>🚗 Zero Tolerance Policy <small>(City of Dallas Ord. 29696; Sec. 47A-2.1.6 & 47A-2.1.7)</small></h3>
          <p>
            FairFare Transportation maintains an <strong>operating authority zero-tolerance policy</strong> for intoxicating substances.
            <strong> Drivers are strictly prohibited</strong> from using drugs or alcohol while providing transportation services
            or immediately before operating a vehicle.
          </p>
          <p>
            If you suspect your driver is under the influence of drugs or alcohol, <strong>end the trip immediately</strong>.
            To report a complaint to the City of Dallas, dial <strong>3-1-1</strong> (or <strong>214-670-3111</strong> from outside Dallas)
            pursuant to <strong>Ord. 29696</strong>. In an emergency, call <strong>911</strong>.
          </p>
          <p>
            Any violation of this Zero Tolerance Policy will result in <strong>immediate suspension</strong> of the driver and an internal
            investigation consistent with City of Dallas Transportation-for-Hire regulations.
          </p>
        </div>

        <div className="policy-item">
          <h3>🔐 Privacy Policy</h3>
          <p>
            We value your privacy. Your personal information is <strong>kept confidential</strong> and only shared with trusted partners
            when necessary to provide you with our services. By using this website, you consent to our data policies.
          </p>
        </div>
      </section>

      {/* Accessibility & Wheelchair Services */}
      <section className="accessibility">
        <h2>Accessibility & Wheelchair Services <small>(Dallas Code Sec. 47A-2.1.7)</small></h2>
        <p>
          FairFare Transportation is committed to accessible service. <strong>Wheelchair-accessible vehicles (WAVs) are available upon request.</strong>
          To request a WAV, please select the “Wheelchair Accessible” option when booking or call us at <strong>469-835-7520</strong> or <strong>469-268-8239</strong>.
          Our drivers provide trained assistance with safe securement and boarding. Advance notice is recommended so we can assign the right vehicle
          and ensure an on-time pickup.
        </p>
        <p>
          Complaints or concerns may also be reported to the City of Dallas by dialing <strong>3-1-1</strong> (or <strong>214-670-3111</strong> outside Dallas)
          in accordance with <strong>Ord. 29696</strong>.
        </p>
      </section>
    </div>
  );
}
