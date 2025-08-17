import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'

import { AuthProvider } from './contexts/AuthContext.tsx'
import ConditionalRouter from './ConditionalRouter.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AuthProvider>
      <ConditionalRouter/>
    </AuthProvider>
  </StrictMode>,
)
