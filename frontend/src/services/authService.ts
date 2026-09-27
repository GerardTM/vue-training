import api from '@/services/api'
import type { User, UserProfileUpdate } from '@/types/User'

interface LoginResponse {
  token: string
  user: User
}

export const authService = {
  async login(email: string, password: string): Promise<LoginResponse> {
    const response = await api.post<LoginResponse>('/auth/login', {
      email,
      password,
    })

    return response.data
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/users/me')

    return response.data
  },

  async updateCurrentUser(profile: UserProfileUpdate): Promise<User> {
    const response = await api.patch<User>('/users/me', profile)

    return response.data
  },
}
