export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-[url('/bg-city.jpg')] bg-cover bg-center flex items-center justify-center px-4">
      <div className="bg-white/90 backdrop-blur-md rounded-2xl shadow-xl p-6 w-full max-w-2xl">
        {children}
      </div>
    </div>
  );
}