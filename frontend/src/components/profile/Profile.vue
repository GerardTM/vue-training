<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/themeStore'
import { ChevronDown, LogOut, Moon, Sun, User } from 'lucide-vue-next'
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const authStore = useAuthStore()
const themeStore = useThemeStore()
const route = useRoute()

const isUserMenuOpen = ref(false)

const toggleUserMenu = () => {
  isUserMenuOpen.value = !isUserMenuOpen.value
}

const closeUserMenu = () => {
  isUserMenuOpen.value = false
}

const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement

  if (!target.closest('.user-menu')) {
    closeUserMenu()
  }
}

watch(
  () => route.path,
  () => {
    closeUserMenu()
  },
)

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<template>
  <div>
    <div class="user-menu">
      <button
        type="button"
        class="user-menu-trigger"
        :aria-expanded="isUserMenuOpen"
        aria-label="Menu utilisateur"
        @click.stop="toggleUserMenu"
      >
        <div class="user-avatar">
          <img
            v-if="authStore.user?.avatar"
            :src="authStore.user.avatar"
            :alt="`Photo de ${authStore.user.firstName ?? 'votre profil'}`"
          />
          <span v-else>
            {{ authStore.user?.firstName?.charAt(0)?.toUpperCase() ?? 'U' }}
          </span>
        </div>

        <div class="user-info">
          <span class="user-name">
            {{ authStore.user?.firstName }}
            {{ authStore.user?.lastName }}
          </span>

          <span class="user-email">
            {{ authStore.user?.email }}
          </span>
        </div>

        <ChevronDown
          :size="16"
          class="user-menu-chevron"
          :class="{ 'user-menu-chevron-open': isUserMenuOpen }"
        />
      </button>

      <Transition name="user-menu">
        <div v-if="isUserMenuOpen" class="user-dropdown">
          <!-- Header -->
          <div class="user-dropdown-header">
            <div class="user-dropdown-avatar">
              <img
                v-if="authStore.user?.avatar"
                :src="authStore.user.avatar"
                :alt="`Photo de ${authStore.user.firstName ?? 'votre profil'}`"
                class="h-full w-full rounded-xl object-cover"
              />
              <span v-else>
                {{ authStore.user?.firstName?.charAt(0)?.toUpperCase() ?? 'U' }}
              </span>
            </div>

            <div class="user-dropdown-user">
              <span class="user-dropdown-name">
                {{ authStore.user?.firstName }}
                {{ authStore.user?.lastName }}
              </span>

              <span class="user-dropdown-email">
                {{ authStore.user?.email }}
              </span>
            </div>
          </div>

          <div class="user-dropdown-separator" />

          <!-- Profile -->
          <RouterLink to="/profile" class="user-dropdown-item" @click="closeUserMenu">
            <span class="user-dropdown-icon">
              <User :size="17" />
            </span>

            <span class="user-dropdown-label">
              <span>Modifier le profil</span>
              <small>Gérer vos informations</small>
            </span>
          </RouterLink>

          <!-- Dark mode -->
          <button type="button" class="user-dropdown-item" @click="themeStore.toggleDarkMode">
            <span class="user-dropdown-icon">
              <Sun v-if="themeStore.isDark" :size="17" />
              <Moon v-else :size="17" />
            </span>

            <span class="user-dropdown-label">
              <span>Mode sombre</span>
              <small>
                {{ themeStore.isDark ? 'Activé' : 'Désactivé' }}
              </small>
            </span>

            <span class="theme-switch" :class="{ 'theme-switch-active': themeStore.isDark }">
              <span class="theme-switch-thumb" />
            </span>
          </button>

          <div class="user-dropdown-separator" />

          <!-- Logout -->
          <button
            type="button"
            class="user-dropdown-item user-dropdown-logout"
            @click="authStore.logout"
          >
            <span class="user-dropdown-icon">
              <LogOut :size="17" />
            </span>

            <span class="user-dropdown-label">
              <span>Déconnexion</span>
              <small>Fermer votre session</small>
            </span>
          </button>
        </div>
      </Transition>
    </div>
  </div>
</template>
