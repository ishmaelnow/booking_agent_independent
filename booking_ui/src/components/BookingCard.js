export default function BookingCard({ booking }) {
  return (
    <div className="bg-white shadow-md rounded-xl p-4 mb-4 border border-gray-200 hover:shadow-lg transition">
      <div className="text-lg font-semibold text-gray-900">
        {booking.rider_name || "Passenger"}
      </div>
      <div className="text-sm text-gray-600">
        {booking.pickup} → {booking.dropoff}
      </div>
      <div className="mt-2 text-sm">
        <span className="font-medium">Time:</span> {booking.ride_time}
      </div>
      <div className="mt-1 text-sm">
        <span className="font-medium">Fare:</span> ${booking.fare}
      </div>
    </div>
  );
}