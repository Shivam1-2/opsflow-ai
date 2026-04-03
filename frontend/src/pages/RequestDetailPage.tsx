import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getRequest, listRequestAudit } from '../api/requests'
import { ApiError } from '../api/http'
import { StatusMessage } from '../components/common/StatusMessage'
import type { AuditEvent, RequestDetail } from '../types/request'

export function RequestDetailPage() {
  const { requestId } = useParams()
  const [request, setRequest] = useState<RequestDetail | null>(null)
  const [audit, setAudit] = useState<AuditEvent[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!requestId) {
      return
    }
    let cancelled = false
    Promise.all([getRequest(requestId), listRequestAudit(requestId)])
      .then(([detail, auditResponse]) => {
        if (!cancelled) {
          setRequest(detail)
          setAudit(auditResponse.results)
        }
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          if (err instanceof ApiError && err.status === 404) {
            setError('Request not found.')
          } else if (err instanceof ApiError && err.status === 403) {
            setError('You do not have access to this request.')
          } else {
            setError(err instanceof ApiError ? err.message : 'Failed to load request.')
          }
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
  }, [requestId])

  if (loading) {
    return <StatusMessage tone="info" message="Loading request…" />
  }

  if (error || !request) {
    return <StatusMessage tone="error" message={error ?? 'Request unavailable.'} />
  }

  return (
    <div className="detail-layout">
      <section className="detail-card">
        <h2>Request {request.id}</h2>
        <dl className="detail-grid">
          <div>
            <dt>Status</dt>
            <dd>{request.status}</dd>
          </div>
          <div>
            <dt>Priority</dt>
            <dd>{request.priority}</dd>
          </div>
          <div>
            <dt>Source</dt>
            <dd>{request.source}</dd>
          </div>
          <div>
            <dt>Created by</dt>
            <dd>{request.created_by.email}</dd>
          </div>
          <div>
            <dt>Created at</dt>
            <dd>{new Date(request.created_at).toLocaleString()}</dd>
          </div>
          <div>
            <dt>Updated at</dt>
            <dd>{new Date(request.updated_at).toLocaleString()}</dd>
          </div>
        </dl>
        <h3>Original request text</h3>
        <pre className="raw-text">{request.raw_text}</pre>
      </section>
      <section className="detail-card">
        <h3>Audit timeline</h3>
        {audit.length === 0 ? (
          <StatusMessage tone="info" message="No audit events yet." />
        ) : (
          <ul className="audit-list">
            {audit.map((event) => (
              <li key={event.id}>
                <strong>{event.event_type}</strong>
                <span>{new Date(event.created_at).toLocaleString()}</span>
                {event.actor ? <span>{event.actor.email}</span> : null}
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  )
}
