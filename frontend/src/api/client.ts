const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000"
const TOKEN_KEY = "access_token"

// Callback invoked on 401 — set by AuthProvider so we can trigger logout reactively
let _onUnauthorized: () => void = () => {}

export function setUnauthorizedHandler(handler: () => void): void {
  _onUnauthorized = handler
}

// ── Token storage ─────────────────────────────────────────────────────────────

export function getStoredToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function storeToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token)
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY)
}

export function isTokenExpired(token: string): boolean {
  try {
    const base64 = token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/")
    const { exp } = JSON.parse(atob(base64)) as { exp: number }
    return Date.now() >= exp * 1000
  } catch {
    return true
  }
}

// ── Fetch wrappers ────────────────────────────────────────────────────────────

/** For unprotected endpoints (e.g. /auth/exchange) — never sends an auth header. */
export async function unauthFetch(path: string, init: RequestInit = {}): Promise<Response> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(init.headers as Record<string, string> ?? {}),
  }
  return fetch(`${API_BASE}${path}`, { ...init, headers })
}

/** For protected endpoints — attaches JWT and triggers logout on 401. */
export async function apiFetch(path: string, init: RequestInit = {}): Promise<Response> {
  const token = getStoredToken()

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(init.headers as Record<string, string> ?? {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  }

  const res = await fetch(`${API_BASE}${path}`, { ...init, headers })

  if (res.status === 401) {
    clearToken()
    _onUnauthorized()
  }

  return res
}
