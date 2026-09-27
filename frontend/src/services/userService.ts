import api from '@/services/api'
import type { UserCreatePayload } from '@/types/User'

export const userService = {
  async create(user: UserCreatePayload): Promise<void> {
    await api.post('/users', user)
  },
}
