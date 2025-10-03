import React from "react";

export default function PolicySection() {
  return (
    <section className="company-policies">
      <h2>Our Commitment to Safety & Service</h2>
      <div className="policy-item">
        <h3>🚗 Zero Tolerance Policy</h3>
        <p>
          Drivers are strictly prohibited from using drugs or alcohol while providing transportation services.
          Suspect a violation? End the trip and report to <strong>3-1-1</strong> or <strong>214-670-3111</strong>.
        </p>
      </div>
      <div className="policy-item">
        <h3>🔐 Privacy Policy</h3>
        <p>
          Your personal information is <strong>kept confidential</strong> and only shared when necessary to provide service.
        </p>
      </div>
    </section>
  );
}