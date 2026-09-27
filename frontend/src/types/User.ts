export interface User {
  id: string
  email: string
  firstName: string | null
  lastName: string | null
  createdAt: string
  avatar: string | null
}

export type UserProfileUpdate = Pick<User, 'email' | 'firstName' | 'lastName' | 'avatar'>

export type UserRole = 'admin' | 'user'

export interface UserCreatePayload {
  firstName: string
  lastName: string
  email: string
  role: UserRole
  password: string
}
