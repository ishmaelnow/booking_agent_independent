import BookingCard from "../components/BookingCard";

const mockBookings = [
  {
    id: 1,
    rider_name: "Ali",
    pickup: "Downtown",
    dropoff: "Airport",
    ride_time: "10:30 AM",
    fare: "22.50",
  },
  {
    id: 2,
    rider_name: "Zara",
    pickup: "Mall",
    dropoff: "University",
    ride_time: "2:15 PM",
    fare: "15.00",
  },
];

export default function BookingHistory() {
  return (
    <div className="min-h-screen bg-gray-50 px-4 py-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">Your Bookings</h1>
      <div className="space-y-4">
        {mockBookings.map((b) => (
          <BookingCard key={b.id} booking={b} />
        ))}
      </div>
    </div>
  );
}