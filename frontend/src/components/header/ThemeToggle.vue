<script setup lang="ts">
import { useThemeStore } from '@/stores/themeStore'
import { Moon, Sun } from 'lucide-vue-next'

const themeStore = useThemeStore()
</script>

<template>
  <button
    type="button"
    class="icon-button"
    :aria-label="themeStore.isDark ? 'Activer le mode clair' : 'Activer le mode sombre'"
    @click="themeStore.toggleDarkMode"
  >
    <Transition name="theme-icon" mode="out-in">
      <Sun v-if="themeStore.isDark" :key="'sun'" :size="19" />
      <Moon v-else :key="'moon'" :size="19" />
    </Transition>
  </button>
</template>
