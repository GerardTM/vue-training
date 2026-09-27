import { AUTH_TOKEN_STORAGE_KEY } from '@/constants/Constants'
import { authService } from '@/services/authService'
import type { User, UserProfileUpdate } from '@/types/User'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem(AUTH_TOKEN_STORAGE_KEY))
  const user = ref<User | null>(null)

  const isAuthenticated = computed(() => token.value !== null)

  const login = (newToken: string, newUser: User) => {
    token.value = newToken
    user.value = newUser

    localStorage.setItem(AUTH_TOKEN_STORAGE_KEY, newToken)
  }

  const logout = () => {
    token.value = null
    user.value = null

    localStorage.removeItem(AUTH_TOKEN_STORAGE_KEY)
  }

  const updateProfile = async (profile: UserProfileUpdate) => {
    const updatedUser = await authService.updateCurrentUser(profile)
    user.value = updatedUser

    return updatedUser
  }

  const restoreSession = async () => {
    if (!token.value) {
      return false
    }

    try {
      user.value = await authService.getCurrentUser()

      return true
    } catch {
      logout()
      return false
    }
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    logout,
    updateProfile,
    restoreSession,
  }
})
