export const API_BASE = (process.env.REACT_APP_API_BASE_URL || "").replace(/\/+$/, "");

if (!API_BASE) {
  // eslint-disable-next-line no-console
  console.warn("[config] REACT_APP_API_BASE_URL is empty. Set it in .env.local");
}

async function request(method, path, { query, body, headers, signal } = {}) {
  const q = query
    ? "?" +
      Object.entries(query)
        .filter(([, v]) => v !== undefined && v !== null)
        .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`)
        .join("&")
    : "";

  const url = `${API_BASE}${path}${q}`;
  const hdrs = { "Content-Type": "application/json", ...(headers || {}) };

  const res = await fetch(url, { method, headers: hdrs, body: body ? JSON.stringify(body) : undefined, signal });
  const text = await res.text();
  const data = text ? JSON.parse(text) : null;

  if (!res.ok) {
    const detail = (data && data.detail) || (data && data.message) || res.statusText;
    throw new Error(`[${res.status}] ${detail || "Request failed"} @ ${method} ${path}`);
  }
  return data;
}

export const http = {
  get: (path, opts) => request("GET", path, opts),
  post: (path, opts) => request("POST", path, opts),
};
