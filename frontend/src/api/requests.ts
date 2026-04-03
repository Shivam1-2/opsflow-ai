import type {
  AuditEvent,
  PaginatedResponse,
  RequestDetail,
  RequestPriority,
  RequestSummary,
} from '../types/request'
import { apiFetch } from './http'

export async function listRequests(status?: string): Promise<PaginatedResponse<RequestSummary>> {
  const query = status ? `?status=${encodeURIComponent(status)}` : ''
  return apiFetch<PaginatedResponse<RequestSummary>>(`/api/v1/requests/${query}`)
}

export async function createRequest(rawText: string, priority: RequestPriority): Promise<RequestDetail> {
  return apiFetch<RequestDetail>('/api/v1/requests/', {
    method: 'POST',
    body: JSON.stringify({ raw_text: rawText, priority }),
  })
}

export async function getRequest(requestId: string): Promise<RequestDetail> {
  return apiFetch<RequestDetail>(`/api/v1/requests/${requestId}/`)
}

export async function listRequestAudit(requestId: string): Promise<PaginatedResponse<AuditEvent>> {
  return apiFetch<PaginatedResponse<AuditEvent>>(`/api/v1/requests/${requestId}/audit/`)
}
