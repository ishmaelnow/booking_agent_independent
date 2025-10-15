import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import BookRide from "../pages/BookRide";
import FarePreview from "../pages/FarePreview";
import JobsView from "../pages/JobsView";
import BookingHistory from "../pages/BookingHistory";
import RideHistory from "../pages/RideHistory";
import FeedbackForm from "../pages/FeedbackForm"; // ✅ New import
// import CompleteRide from "../pages/CompleteRide"; // 🔒 Driver-only
import DistanceTracker from "../pages/DistanceTracker";
import LiveTracker from "../pages/LiveTracker"; // ✅ New import
import TestBackendPing from "../pages/TestBackendPing"; // ✅ Diagnostic route
import BookRideStandalone from "../pages/BookRideStandalone"; // For testing

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/book" element={<BookRide />} />
        <Route path="/fare-preview" element={<FarePreview />} />
        <Route path="/jobs" element={<JobsView />} />
        <Route path="/bookings" element={<BookingHistory />} />
        <Route path="/history" element={<RideHistory />} />
        <Route path="/feedback" element={<FeedbackForm />} /> {/* ✅ New route */}
        <Route path="/distance" element={<DistanceTracker />} />
        <Route path="/live" element={<LiveTracker pin={985217} />} /> {/* ✅ New route */}
        <Route path="/test-ping" element={<TestBackendPing />} /> {/* ✅ Diagnostic route */}
        {/* <Route path="/complete-ride" element={<CompleteRide />} />  🔒 Driver-only */}
        <Route path="/stand-alone" element={<BookRideStandalone />} /> {/* For testing */}

      </Routes>
    </BrowserRouter>
  );
}