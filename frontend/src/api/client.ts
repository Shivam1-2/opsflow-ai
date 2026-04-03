import type { HealthResponse } from '../types/health'
import { apiFetch } from './http'

export async function getHealth(): Promise<HealthResponse> {
  const payload: unknown = await apiFetch<unknown>('/api/v1/health/')
  if (!isHealthResponse(payload)) {
    throw new Error('Health response was not in the expected format')
  }
  return payload
}

function isHealthResponse(value: unknown): value is HealthResponse {
  return (
    typeof value === 'object' &&
    value !== null &&
    'status' in value &&
    typeof value.status === 'string'
  )
}
