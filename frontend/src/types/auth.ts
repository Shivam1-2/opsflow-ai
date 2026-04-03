export type UserRole = 'ADMIN' | 'OPERATOR' | 'REVIEWER'

export type OrganizationSummary = {
  id: string
  name: string
}

export type CurrentUser = {
  id: string
  email: string
  organization: OrganizationSummary
  role: UserRole
}
