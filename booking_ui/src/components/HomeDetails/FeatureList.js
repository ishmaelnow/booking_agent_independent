import React from "react";

const features = [
  { title: "Quick and Easy Booking", description: "Book your ride in just a few clicks." },
  { title: "Affordable Pricing", description: "Get the best rates for your journeys." },
  { title: "Safe and Reliable", description: "All our drivers are verified and professional." },
  { title: "24/7 Service", description: "Available anytime you need a ride in the Dallas/Fort Worth area." },
  { title: "Wheelchair Accessible", description: "Wheelchair-accessible vehicles are available upon request." },
];

export default function FeatureList() {
  return (
    <section className="features">
      <h2>Why Choose Us?</h2>
      <ul>
        {features.map(({ title, description }) => (
          <li key={title}>
            <h3>{title}</h3>
            <p>{description}</p>
          </li>
        ))}
      </ul>
    </section>
  );
}