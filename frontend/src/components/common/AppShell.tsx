import { Link, Outlet } from 'react-router-dom'
import type { CurrentUser } from '../../types/auth'

type AppShellProps = {
  user: CurrentUser
  onLogout: () => Promise<void>
}

export function AppShell({ user, onLogout }: AppShellProps) {
  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <h1>OpsFlow AI</h1>
          <p className="lede">Operations workflow</p>
        </div>
        <div className="user-panel">
          <p>{user.email}</p>
          <p>
            {user.organization.name} · {user.role}
          </p>
          <button type="button" onClick={() => void onLogout()}>
            Log out
          </button>
        </div>
      </header>
      <nav className="app-nav">
        <Link to="/requests">Requests</Link>
        {(user.role === 'ADMIN' || user.role === 'OPERATOR') && (
          <Link to="/requests/new">New request</Link>
        )}
      </nav>
      <main className="app-main">
        <Outlet />
      </main>
    </div>
  )
}
