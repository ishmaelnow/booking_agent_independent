import { useState } from "react";
import { getFareEstimate } from "../api/fare";
import Header from "../components/Header";
import { FaChartLine } from "react-icons/fa";

export default function FarePreview() {
  const [miles, setMiles] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleEstimate = async () => {
    setError("");
    setResult(null);

    const milesNum = parseFloat(miles);
    if (Number.isNaN(milesNum) || milesNum <= 0) {
      setError("Please enter a valid number of miles greater than 0.");
      return;
    }

    setLoading(true);
    try {
      const res = await getFareEstimate(milesNum, { explain: true });
      console.log("Fare estimate response:", res.data);
      setResult(res.data);
    } catch (err) {
      console.error("Fare estimate error:", err);
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        "Unable to fetch fare estimate.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[url('/bg.jpg')] bg-cover bg-center flex items-center justify-center px-4">
      <div className="bg-white/80 backdrop-blur-lg shadow-2xl rounded-2xl p-6 w-full max-w-md">
        <Header />

        <div className="flex items-center gap-2 mb-6">
          <FaChartLine className="text-xl text-gray-700" />
          <h1 className="text-2xl font-bold text-gray-900">Fare Preview</h1>
        </div>

        <input
          type="number"
          min="0"
          step="0.1"
          className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-black mb-3"
          placeholder="Enter distance in miles"
          value={miles}
          onChange={(e) => setMiles(e.target.value)}
        />

        {error && (
          <div className="mb-3 rounded-xl bg-red-50 border border-red-200 p-3 text-red-700 text-sm">
            ⚠️ {error}
          </div>
        )}

        <button
          type="button"
          onClick={handleEstimate}
          disabled={loading || !miles}
          className={`w-full py-3 rounded-xl text-white font-semibold transition ${
            loading ? "bg-gray-400 cursor-not-allowed" : "bg-black hover:bg-gray-800"
          }`}
        >
          {loading ? "Estimating…" : "Get Fare Estimate"}
        </button>

        {result && (
          <div className="mt-6 bg-gray-100 p-4 rounded-xl shadow text-gray-800">
            {typeof result.fare_estimate !== "undefined" && (
              <p className="text-lg font-medium">
                Estimated Fare: <span className="text-black">${result.fare_estimate}</span>
              </p>
            )}
            {typeof result.input_miles !== "undefined" && (
              <p className="text-sm mt-1">
                Distance: <strong>{Number(result.input_miles).toFixed(2)} mi</strong>
              </p>
            )}
            {result.fare_explanation && (
              <p className="mt-2 text-sm text-gray-700">
                <strong>Note:</strong> {result.fare_explanation}
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}