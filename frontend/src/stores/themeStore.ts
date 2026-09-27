import { THEME_STORAGE_KEY } from '@/constants/Constants'
import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const savedTheme = localStorage.getItem(THEME_STORAGE_KEY)

  const isDark = ref(
    savedTheme ? savedTheme === 'dark' : window.matchMedia('(prefers-color-scheme: dark)').matches,
  )

  const applyTheme = (dark: boolean) => {
    document.documentElement.classList.toggle('dark', dark)
  }

  const toggleDarkMode = () => {
    isDark.value = !isDark.value
  }

  // Applique le thème initial
  applyTheme(isDark.value)

  // Sauvegarde le choix de l'utilisateur
  watch(isDark, (dark) => {
    localStorage.setItem(THEME_STORAGE_KEY, dark ? 'dark' : 'light')
    applyTheme(dark)
  })

  return {
    isDark,
    toggleDarkMode,
  }
})
