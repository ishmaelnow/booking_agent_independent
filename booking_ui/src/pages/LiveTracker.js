import React, { useEffect, useMemo, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import api from "../api/booking"; // ✅ Centralized axios instance

const riderIcon = L.icon({
  iconUrl: "/icons/rider.png",
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

const driverIcon = L.icon({
  iconUrl: "/icons/driver.png",
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

const getDistanceMiles = (lat1, lng1, lat2, lng2) => {
  const R = 3958.8;
  const toRad = (d) => (d * Math.PI) / 180;
  const dLat = toRad(lat2 - lat1);
  const dLng = toRad(lng2 - lng1);
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLng / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
};

function useQuery() {
  const { search } = useLocation();
  return useMemo(() => new URLSearchParams(search), [search]);
}

const LiveTracker = ({ pin: propPin }) => {
  const query = useQuery();
  const navigate = useNavigate();

  const pinRaw = propPin ?? query.get("pin") ?? "";
  const pin = /^\d+$/.test(String(pinRaw)) ? String(pinRaw) : "";

  const [locations, setLocations] = useState({});
  const [distanceMiles, setDistanceMiles] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const defaultCenter = { lat: 32.7767, lng: -96.7970 };

  const center = useMemo(() => {
    if (locations?.rider?.lat && locations?.rider?.lng) {
      return { lat: locations.rider.lat, lng: locations.rider.lng };
    }
    if (locations?.driver?.lat && locations?.driver?.lng) {
      return { lat: locations.driver.lat, lng: locations.driver.lng };
    }
    return defaultCenter;
  }, [locations]);

  useEffect(() => {
    if (!pin) {
      setError("Missing or invalid PIN.");
      setLoading(false);
      return;
    }

    let cancelled = false;

    const fetchLive = async () => {
      try {
        const res = await api.get("/track/live", {
          params: { pin },
          timeout: 8000,
        });
        if (cancelled) return;

        const data = res.data || {};
        setLocations(data);
        setError("");

        const { rider, driver } = data;
        if (rider && driver && rider.lat && rider.lng && driver.lat && driver.lng) {
          setDistanceMiles(getDistanceMiles(rider.lat, rider.lng, driver.lat, driver.lng));
        } else {
          setDistanceMiles(null);
        }
      } catch (err) {
        if (cancelled) return;
        console.error("Live tracking error:", err);
        setError("Unable to fetch live locations.");
        setLocations({});
        setDistanceMiles(null);
      } finally {
        if (!cancelled) setLoading(false);
      }
    };

    fetchLive();
    const id = setInterval(fetchLive, 5000);
    return () => {
      cancelled = true;
      clearInterval(id);
    };
  }, [pin]);

  const renderMarker = (role, data) => (
    <Marker
      key={role}
      position={[data.lat, data.lng]}
      icon={role === "rider" ? riderIcon : driverIcon}
    >
      <Popup>
        <strong>{role.toUpperCase()}</strong>
        <br />
        Lat: {data.lat}
        <br />
        Lng: {data.lng}
        <br />
        Time: {new Date(data.timestamp).toLocaleTimeString()}
      </Popup>
    </Marker>
  );

  return (
    <div style={{ padding: 20 }}>
      <button
        onClick={() => navigate("/")}
        style={{
          padding: "10px 20px",
          marginBottom: 20,
          backgroundColor: "#111",
          color: "#fff",
          border: "none",
          borderRadius: 8,
          cursor: "pointer",
        }}
      >
        ⬅️ Back to Home
      </button>

      {!pin && <p style={{ color: "red" }}>Provide a numeric PIN in the URL, e.g. <code>/live?pin=0042</code></p>}
      {loading && <p>Loading live locations…</p>}
      {error && !loading && <p style={{ color: "red" }}>⚠️ {error}</p>}

      {distanceMiles !== null && (
        <p style={{ fontSize: 18, marginBottom: 10 }}>
          📏 Driver is <strong>{distanceMiles.toFixed(2)} miles</strong> from Rider
        </p>
      )}

      <MapContainer
        center={[center.lat, center.lng]}
        zoom={12}
        scrollWheelZoom
        style={{ height: 500, width: "100%" }}
      >
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {locations.driver && renderMarker("driver", locations.driver)}
        {locations.rider && renderMarker("rider", locations.rider)}
      </MapContainer>

      {!loading && !error && !locations.driver && !locations.rider && (
        <p style={{ marginTop: 12 }}>
          No live location yet for PIN <strong>{pin}</strong>. Try again in a moment.
        </p>
      )}
    </div>
  );
};

export default LiveTracker;