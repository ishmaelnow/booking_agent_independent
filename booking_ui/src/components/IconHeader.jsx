// src/components/IconHeader.jsx
import { FaChartLine } from "react-icons/fa";

export default function IconHeader({ title }) {
  return (
    <div className="flex items-center gap-2 mb-6">
      <FaChartLine className="text-xl text-gray-700" />
      <h2 className="text-2xl font-bold text-gray-900">{title}</h2>
    </div>
  );
}