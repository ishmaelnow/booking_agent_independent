import { Link } from "react-router-dom";

export default function Header() {
  return (
    <div className="w-full bg-gray-100 py-2 px-4 mb-4 text-center">
      <Link to="/" className="text-blue-600 font-medium hover:underline">
        ← Back to Home
      </Link>
    </div>
  );
}