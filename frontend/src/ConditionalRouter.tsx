import App from "./App.tsx"
import PhoneAuth from "./components/PhoneAuth.tsx"
import { useAuth } from "./contexts/AuthContext.tsx"

export default function ConditionalRouter() {
  const { isAuthenticated, loading } = useAuth()

  if (loading) return <p>Loading...</p>

  if (!isAuthenticated) return <PhoneAuth />

  return <App />
}
