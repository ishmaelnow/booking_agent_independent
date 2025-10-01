// src/components/Button.js
export default function Button({ children, onClick, type = "button", variant = "primary" }) {
  return (
    <button onClick={onClick} type={type} className={`btn ${variant}`}>
      {children}
    </button>
  );
}