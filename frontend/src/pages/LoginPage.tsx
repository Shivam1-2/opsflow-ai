import { useState } from 'react'
import type { FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { login } from '../api/auth'
import { ApiError } from '../api/http'
import { StatusMessage } from '../components/common/StatusMessage'

type LoginPageProps = {
  onAuthenticated: () => Promise<void>
}

export function LoginPage({ onAuthenticated }: LoginPageProps) {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    setLoading(true)
    setError(null)
    try {
      await login(email, password)
      await onAuthenticated()
      navigate('/requests')
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError('Network error. Check that the backend is running.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="page page--narrow">
      <h1>Sign in</h1>
      <p className="lede">OpsFlow AI operations inbox</p>
      <form className="form-card" onSubmit={(event) => void handleSubmit(event)}>
        <label>
          Email
          <input
            type="email"
            autoComplete="username"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
        </label>
        <label>
          Password
          <input
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />
        </label>
        {error ? <StatusMessage tone="error" message={error} /> : null}
        <button type="submit" disabled={loading}>
          {loading ? 'Signing in…' : 'Sign in'}
        </button>
      </form>
    </main>
  )
}
