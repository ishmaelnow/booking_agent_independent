import { useState } from "react";
import { getFareEstimate } from "../api/fare";
import Header from "../components/Header";
import { FaChartLine } from "react-icons/fa"; // Icon for visual polish

export default function FarePreview() {
  const [miles, setMiles] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleEstimate = async () => {
    setLoading(true);
    try {
      const res = await getFareEstimate(miles);
      console.log("Fare estimate response:", res.data);
      setResult(res.data);
    } catch (error) {
      console.error("Fare estimate failed:", error);
      setResult({ error: "Unable to fetch fare estimate." });
    }
    setLoading(false);
  };

  return (
    // 🔳 Fullscreen background with centered glass card
    <div className="min-h-screen bg-[url('/bg.jpg')] bg-cover bg-center flex items-center justify-center px-4">
      
      {/* 🧊 Glassmorphic card container */}
      <div className="bg-white/80 backdrop-blur-lg shadow-2xl rounded-2xl p-6 w-full max-w-md">
        
        {/* 🧭 Optional global header */}
        <Header />

        {/* 📈 Heading with icon */}
        <div className="flex items-center gap-2 mb-6">
          <FaChartLine className="text-xl text-gray-700" />
          <h1 className="text-2xl font-bold text-gray-900">Fare Preview</h1>
        </div>

        {/* 📥 Input field */}
        <input
          type="number"
          className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-black mb-4"
          placeholder="Enter distance in miles"
          value={miles}
          onChange={(e) => setMiles(e.target.value)}
        />

        {/* 🚀 Submit button */}
        <button
          type="button"
          onClick={handleEstimate}
          disabled={loading || !miles}
          className={`w-full py-3 rounded-xl text-white font-semibold transition ${
            loading ? "bg-gray-400" : "bg-black hover:bg-gray-800"
          }`}
        >
          {loading ? "Estimating..." : "Get Fare Estimate"}
        </button>

        {/* 📊 Result display */}
        {result && (
          <div className="mt-6 bg-gray-100 p-4 rounded-xl shadow">
            {result.error ? (
              <p className="text-red-600">{result.error}</p>
            ) : (
              <>
                {result.fare_estimate !== undefined && (
                  <p className="text-lg font-medium text-gray-800">
                    Estimated Fare: <span className="text-black">${result.fare_estimate}</span>
                  </p>
                )}
                {result.fare_explanation && (
                  <p className="mt-2 text-sm text-gray-700">
                    <strong>Explanation:</strong> {result.fare_explanation}
                  </p>
                )}
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}