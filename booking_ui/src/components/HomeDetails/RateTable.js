import React from "react";

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

export default function RateTable() {
  return (
    <section className="rates">
      <h2>Taxi Cab Rates</h2>
      <table className="rate-table">
        <thead>
          <tr><th>Service</th><th>Rate</th></tr>
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
  );
}