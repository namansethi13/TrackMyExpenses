import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
  type ReactNode,
} from "react"
import { onAuthStateChanged, signOut, type User } from "firebase/auth"

import { auth } from "@/firebase"
import { exchangeFirebaseToken } from "@/api/service"
import {
  clearToken,
  getStoredToken,
  isTokenExpired,
  setUnauthorizedHandler,
  storeToken,
} from "@/api/client"

// ── Types ─────────────────────────────────────────────────────────────────────

type AuthContextType = {
  isAuthenticated: boolean
  accessToken: string | null
  firebaseUser: User | null
  loading: boolean
  logout: () => Promise<void>
}

// ── Context ───────────────────────────────────────────────────────────────────

const AuthContext = createContext<AuthContextType | undefined>(undefined)

// ── Provider ──────────────────────────────────────────────────────────────────

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [accessToken, setAccessToken] = useState<string | null>(null)
  const [firebaseUser, setFirebaseUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  const logoutTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  // ── logout ─────────────────────────────────────────────────────────────────

  const logout = useCallback(async () => {
    if (logoutTimerRef.current) clearTimeout(logoutTimerRef.current)
    clearToken()
    setAccessToken(null)
    setIsAuthenticated(false)
    setFirebaseUser(null)
    try {
      await signOut(auth)
    } catch {
      // Firebase signOut failure is non-fatal
    }
  }, [])

  // ── Auto-logout when JWT expires ───────────────────────────────────────────

  const scheduleAutoLogout = useCallback(
    (token: string) => {
      if (logoutTimerRef.current) clearTimeout(logoutTimerRef.current)
      try {
        const base64 = token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/")
        const { exp } = JSON.parse(atob(base64)) as { exp: number }
        const msUntilExpiry = exp * 1000 - Date.now()
        if (msUntilExpiry <= 0) {
          logout()
          return
        }
        logoutTimerRef.current = setTimeout(logout, msUntilExpiry)
      } catch {
        logout()
      }
    },
    [logout],
  )

  // ── Register 401 handler so API layer can trigger logout reactively ────────

  useEffect(() => {
    setUnauthorizedHandler(logout)
  }, [logout])

  // ── Auth initialization ────────────────────────────────────────────────────

  useEffect(() => {
    // Fast path: valid JWT already in localStorage — skip Firebase listener
    const storedToken = getStoredToken()
    if (storedToken && !isTokenExpired(storedToken)) {
      setAccessToken(storedToken)
      setIsAuthenticated(true)
      setLoading(false)
      scheduleAutoLogout(storedToken)
      return
    }

    // No valid JWT — wait for Firebase auth state, then exchange for our JWT
    clearToken()

    const unsubscribe = onAuthStateChanged(auth, async (fbUser) => {
      setFirebaseUser(fbUser)

      if (fbUser) {
        try {
          const idToken = await fbUser.getIdToken()
          const jwt = await exchangeFirebaseToken(idToken)
          storeToken(jwt)
          setAccessToken(jwt)
          setIsAuthenticated(true)
          scheduleAutoLogout(jwt)
        } catch {
          setIsAuthenticated(false)
        }
      } else {
        setIsAuthenticated(false)
      }

      setLoading(false)
    })

    return () => unsubscribe()
  }, [logout, scheduleAutoLogout])

  return (
    <AuthContext.Provider
      value={{ isAuthenticated, accessToken, firebaseUser, loading, logout }}
    >
      {children}
    </AuthContext.Provider>
  )
}

// ── Hook ──────────────────────────────────────────────────────────────────────

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) throw new Error("useAuth must be used inside AuthProvider")
  return context
}
