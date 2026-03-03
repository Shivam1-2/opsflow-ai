import type { HealthResponse } from '../types/health'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export async function getHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/health/`)

  if (!response.ok) {
    throw new Error(`Health request failed with status ${response.status}`)
  }

  const payload: unknown = await response.json()
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
