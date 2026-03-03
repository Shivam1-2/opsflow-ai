import { useEffect, useState } from 'react'
import { getHealth } from '../api/client'

type BackendStatus = 'checking' | 'connected' | 'unavailable'

export function HomePage() {
  const [backendStatus, setBackendStatus] = useState<BackendStatus>('checking')

  useEffect(() => {
    let cancelled = false

    getHealth()
      .then((health) => {
        if (!cancelled) {
          setBackendStatus(health.status === 'ok' ? 'connected' : 'unavailable')
        }
      })
      .catch(() => {
        if (!cancelled) {
          setBackendStatus('unavailable')
        }
      })

    return () => {
      cancelled = true
    }
  }, [])

  const backendLabel =
    backendStatus === 'connected'
      ? 'Connected'
      : backendStatus === 'unavailable'
        ? 'Unavailable'
        : 'Checking…'

  return (
    <main className="page">
      <h1>OpsFlow AI</h1>
      <p className="lede">AI-powered operations workflow platform</p>
      <section className="status-card">
        <h2>System Status</h2>
        <p>Backend: {backendLabel}</p>
      </section>
    </main>
  )
}
