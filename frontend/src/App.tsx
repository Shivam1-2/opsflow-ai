import { useCallback, useEffect, useState } from 'react'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { getCurrentUser, logout } from './api/auth'
import { AppShell } from './components/common/AppShell'
import { LoginPage } from './pages/LoginPage'
import { RequestCreatePage } from './pages/RequestCreatePage'
import { RequestDetailPage } from './pages/RequestDetailPage'
import { RequestListPage } from './pages/RequestListPage'
import type { CurrentUser } from './types/auth'

function AppRoutes() {
  const [user, setUser] = useState<CurrentUser | null>(null)
  const [bootstrapping, setBootstrapping] = useState(true)

  const refreshUser = useCallback(async () => {
    try {
      const current = await getCurrentUser()
      setUser(current)
    } catch {
      setUser(null)
    }
  }, [])

  useEffect(() => {
    void refreshUser().finally(() => setBootstrapping(false))
  }, [refreshUser])

  async function handleLogout() {
    await logout()
    setUser(null)
  }

  if (bootstrapping) {
    return <main className="page">Loading…</main>
  }

  return (
    <Routes>
      <Route
        path="/login"
        element={user ? <Navigate to="/requests" replace /> : <LoginPage onAuthenticated={refreshUser} />}
      />
      <Route
        path="/"
        element={
          user ? (
            <AppShell user={user} onLogout={handleLogout} />
          ) : (
            <Navigate to="/login" replace />
          )
        }
      >
        <Route index element={<Navigate to="/requests" replace />} />
        <Route path="requests" element={<RequestListPage />} />
        <Route path="requests/new" element={<RequestCreatePage />} />
        <Route path="requests/:requestId" element={<RequestDetailPage />} />
      </Route>
      <Route path="*" element={<Navigate to={user ? '/requests' : '/login'} replace />} />
    </Routes>
  )
}

function App() {
  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  )
}

export default App
