import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import BookRide from "../pages/BookRide";
import FarePreview from "../pages/FarePreview";
import JobsView from "../pages/JobsView";
import BookingHistory from "../pages/BookingHistory";
import RideHistory from "../pages/RideHistory";
// import CompleteRide from "../pages/CompleteRide"; // 🔒 Driver-only

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/book" element={<BookRide />} />
        <Route path="/fare-preview" element={<FarePreview />} />
        <Route path="/jobs" element={<JobsView />} />
        <Route path="/bookings" element={<BookingHistory />} />
        {/* <Route path="/complete" element={<CompleteRide />} /> */}
        {<Route path="/history" element={<RideHistory />} />}
      </Routes>
    </BrowserRouter>
  );
}