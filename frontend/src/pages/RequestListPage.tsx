import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listRequests } from '../api/requests'
import { ApiError } from '../api/http'
import { StatusMessage } from '../components/common/StatusMessage'
import type { RequestSummary } from '../types/request'

export function RequestListPage() {
  const [requests, setRequests] = useState<RequestSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    listRequests()
      .then((response) => {
        if (!cancelled) {
          setRequests(response.results)
        }
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          setError(err instanceof ApiError ? err.message : 'Failed to load requests.')
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoading(false)
        }
      })
    return () => {
      cancelled = true
    }
  }, [])

  if (loading) {
    return <StatusMessage tone="info" message="Loading requests…" />
  }

  if (error) {
    return <StatusMessage tone="error" message={error} />
  }

  if (requests.length === 0) {
    return <StatusMessage tone="info" message="No requests yet." />
  }

  return (
    <section className="table-card">
      <h2>Requests</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Created</th>
            <th>Status</th>
            <th>Priority</th>
            <th>Source</th>
            <th>Creator</th>
          </tr>
        </thead>
        <tbody>
          {requests.map((request) => (
            <tr key={request.id}>
              <td>
                <Link to={`/requests/${request.id}`}>{request.id.slice(0, 8)}…</Link>
              </td>
              <td>{new Date(request.created_at).toLocaleString()}</td>
              <td>{request.status}</td>
              <td>{request.priority}</td>
              <td>{request.source}</td>
              <td>{request.created_by.email}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  )
}
