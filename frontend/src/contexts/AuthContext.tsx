import { auth } from "@/firebase"
import { onAuthStateChanged, type User } from "firebase/auth"
import { createContext, useEffect, useState, type ReactNode , useContext} from "react"
type AuthContextType = {
    user : User | null, 
    loading : boolean
    setUser: (user : User | null) => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({children} : {children : ReactNode}) => {
    let [user, setUser] = useState<User | null>(null);
    let [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        const unsubscribe =  onAuthStateChanged(auth, (firebaseUser) => {
            setUser(firebaseUser);
            firebaseUser?.getIdToken().then((idToken) => {
                console.log("id token: ", idToken);
            });
            setLoading(false);
        })
        
        return () => unsubscribe()
    }, [])


    return (
        <AuthContext.Provider value={{user, loading, setUser}}>
            {children}
        </AuthContext.Provider>
    )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider")
  }
  return context
}