import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// ✅ Custom Icons
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

// ✅ Haversine formula in miles
const getDistanceMiles = (lat1, lng1, lat2, lng2) => {
  const R = 3958.8; // Earth radius in miles
  const dLat = (lat2 - lat1) * (Math.PI / 180);
  const dLng = (lng2 - lng1) * (Math.PI / 180);
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(lat1 * (Math.PI / 180)) *
      Math.cos(lat2 * (Math.PI / 180)) *
      Math.sin(dLng / 2) ** 2;
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
};

const LiveTracker = ({ pin }) => {
  const [locations, setLocations] = useState({});
  const [error, setError] = useState(null);
  const [distanceMiles, setDistanceMiles] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchLiveLocations = async () => {
      try {
        const res = await axios.get(`http://localhost:8000/track/live?pin=${pin}`);
        setLocations(res.data);
        setError(null);

        const { rider, driver } = res.data;
        if (rider && driver) {
          const dist = getDistanceMiles(rider.lat, rider.lng, driver.lat, driver.lng);
          setDistanceMiles(dist);
        } else {
          setDistanceMiles(null);
        }
      } catch (err) {
        setError("Unable to fetch live locations.");
        setLocations({});
        setDistanceMiles(null);
      }
    };

    fetchLiveLocations();
    const interval = setInterval(fetchLiveLocations, 5000);
    return () => clearInterval(interval);
  }, [pin]);

  const renderMarker = (role, data) => {
    const icon = role === "rider" ? riderIcon : driverIcon;

    return (
      <Marker key={role} position={[data.lat, data.lng]} icon={icon}>
        <Popup>
          <strong>{role.toUpperCase()}</strong><br />
          Lat: {data.lat}<br />
          Lng: {data.lng}<br />
          Time: {new Date(data.timestamp).toLocaleTimeString()}
        </Popup>
      </Marker>
    );
  };

  const center = locations.rider || locations.driver || { lat: 32.7767, lng: -96.7970 };

  return (
    <div style={{ padding: "20px" }}>
      <button
        onClick={() => navigate("/")}
        style={{
          padding: "10px 20px",
          marginBottom: "20px",
          backgroundColor: "#28a745",
          color: "#fff",
          border: "none",
          borderRadius: "6px",
          cursor: "pointer"
        }}
      >
        ⬅️ Back to Home
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {distanceMiles !== null && (
        <p style={{ fontSize: "18px", marginBottom: "10px" }}>
          📏 Driver is <strong>{distanceMiles.toFixed(2)} miles</strong> from Rider
        </p>
      )}

      <MapContainer center={[center.lat, center.lng]} zoom={12} scrollWheelZoom={true} style={{ height: "500px", width: "100%" }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {locations.driver && renderMarker("driver", locations.driver)}
        {locations.rider && renderMarker("rider", locations.rider)}
      </MapContainer>
    </div>
  );
};

export default LiveTracker;