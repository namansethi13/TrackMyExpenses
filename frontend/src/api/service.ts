/**
 * service.ts — single source of truth for all backend API calls.
 *
 * Unprotected routes  → unauthFetch  (no Authorization header)
 * Protected routes    → apiFetch     (attaches JWT, triggers logout on 401)
 *
 * Add new backend calls here as the app grows.
 */

import { apiFetch, unauthFetch } from "./client"

// ── Auth ──────────────────────────────────────────────────────────────────────

export async function exchangeFirebaseToken(firebaseToken: string): Promise<string> {
  const res = await unauthFetch("/auth/exchange", {
    method: "POST",
    body: JSON.stringify({ firebase_token: firebaseToken }),
  })

  if (!res.ok) throw new Error(`Token exchange failed: ${res.status}`)

  const data = await res.json()
  return data.access_token as string
}

// ── Expenses (future) ─────────────────────────────────────────────────────────

// export async function getExpenses() { ... }
// export async function createExpense(payload: CreateExpenseRequest) { ... }
