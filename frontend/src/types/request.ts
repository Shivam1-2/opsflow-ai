export type RequestPriority = 'LOW' | 'NORMAL' | 'HIGH' | 'URGENT'
export type RequestSource = 'TEXT' | 'DOCUMENT'
export type RequestStatus =
  | 'RECEIVED'
  | 'PROCESSING'
  | 'EXTRACTED'
  | 'VALIDATING'
  | 'PENDING_REVIEW'
  | 'FAILED'
  | 'REJECTED'
  | 'APPROVED'
  | 'EXECUTING'
  | 'COMPLETED'

export type UserSummary = {
  id: string
  email: string
}

export type RequestSummary = {
  id: string
  source: RequestSource
  priority: RequestPriority
  status: RequestStatus
  created_by: UserSummary
  created_at: string
  updated_at: string
}

export type RequestDetail = RequestSummary & {
  raw_text: string
  source_reference: string
  received_at: string | null
}

export type PaginatedResponse<T> = {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export type AuditEvent = {
  id: string
  event_type: string
  metadata: Record<string, unknown>
  actor: UserSummary | null
  created_at: string
}
