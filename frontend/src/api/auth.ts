import type { CurrentUser } from '../types/auth'
import { apiFetch } from './http'

export async function ensureCsrfCookie(): Promise<void> {
  await apiFetch<{ detail: string }>('/api/v1/auth/csrf/')
}

export async function login(email: string, password: string): Promise<CurrentUser> {
  await ensureCsrfCookie()
  return apiFetch<CurrentUser>('/api/v1/auth/login/', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
}

export async function logout(): Promise<void> {
  await apiFetch<void>('/api/v1/auth/logout/', { method: 'POST' })
}

export async function getCurrentUser(): Promise<CurrentUser> {
  return apiFetch<CurrentUser>('/api/v1/auth/me/')
}
