import { useState } from "react";

export default function DriverLogin({ onLogin }) {
  const [pin, setPin] = useState("");

  const handleSubmit = async () => {
    const res = await fetch(`/drivers/history?pin=${pin}`);
    const data = await res.json();
    onLogin(data.history);
  };

  return (
    <div className="p-4 bg-white shadow rounded">
      <h2 className="text-xl font-bold mb-2">Driver Access</h2>
      <input
        type="text"
        placeholder="Enter Driver PIN"
        value={pin}
        onChange={(e) => setPin(e.target.value)}
        className="border p-2 w-full mb-2"
      />
      <button onClick={handleSubmit} className="bg-blue-600 text-white px-4 py-2 rounded">
        View History
      </button>
    </div>
  );
}