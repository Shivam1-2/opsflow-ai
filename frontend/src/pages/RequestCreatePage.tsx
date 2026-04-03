import { useState } from 'react'
import type { FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { createRequest } from '../api/requests'
import { ApiError } from '../api/http'
import { StatusMessage } from '../components/common/StatusMessage'
import type { RequestPriority } from '../types/request'

const PRIORITIES: RequestPriority[] = ['LOW', 'NORMAL', 'HIGH', 'URGENT']

export function RequestCreatePage() {
  const navigate = useNavigate()
  const [rawText, setRawText] = useState('')
  const [priority, setPriority] = useState<RequestPriority>('NORMAL')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    setLoading(true)
    setError(null)
    try {
      const created = await createRequest(rawText, priority)
      navigate(`/requests/${created.id}`)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Failed to create request.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="form-card">
      <h2>New request</h2>
      <form onSubmit={(event) => void handleSubmit(event)}>
        <label>
          Request text
          <textarea
            value={rawText}
            onChange={(event) => setRawText(event.target.value)}
            rows={8}
            required
          />
        </label>
        <label>
          Priority
          <select value={priority} onChange={(event) => setPriority(event.target.value as RequestPriority)}>
            {PRIORITIES.map((value) => (
              <option key={value} value={value}>
                {value}
              </option>
            ))}
          </select>
        </label>
        {error ? <StatusMessage tone="error" message={error} /> : null}
        <button type="submit" disabled={loading}>
          {loading ? 'Submitting…' : 'Create request'}
        </button>
      </form>
    </section>
  )
}
