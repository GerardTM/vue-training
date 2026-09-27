<script setup lang="ts">
import { ClipboardList, FileInput, FileText, Home, ScrollText } from 'lucide-vue-next'

import { nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const navbar = ref<HTMLElement | null>(null)
const indicator = ref<HTMLElement | null>(null)

const isMobileMenuOpen = ref(false)

const links = [
  {
    to: '/',
    label: 'Accueil',
    icon: Home,
  },
  {
    to: '/referentiel',
    label: 'Référentiel',
    icon: ClipboardList,
  },
  {
    to: '/import',
    label: 'Imports',
    icon: FileInput,
  },
  {
    to: '/product',
    label: 'Articles',
    icon: FileText,
  },
  {
    to: '/logs',
    label: 'Logs',
    icon: ScrollText,
  },
]

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

const updateIndicator = async () => {
  await nextTick()

  if (!navbar.value || !indicator.value) return

  const activeLink = navbar.value.querySelector('.nav-link-active') as HTMLElement | null

  if (!activeLink) return

  const navbarRect = navbar.value.getBoundingClientRect()
  const linkRect = activeLink.getBoundingClientRect()

  indicator.value.style.width = `${linkRect.width}px`
  indicator.value.style.transform = `translateX(${linkRect.left - navbarRect.left}px)`
}

const handleResize = () => {
  updateIndicator()
}

watch(
  () => route.path,
  () => {
    updateIndicator()
    closeMobileMenu()
  },
)

onMounted(() => {
  updateIndicator()

  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <div class="navbar-wrapper">
    <!-- Desktop -->
    <nav ref="navbar" class="navbar">
      <div ref="indicator" class="nav-indicator" />

      <RouterLink
        v-for="link in links"
        :key="link.to"
        :to="link.to"
        class="nav-link"
        :exact-active-class="link.to === '/' ? 'nav-link-active' : undefined"
        active-class="nav-link-active"
      >
        <component :is="link.icon" :size="17" />
        <span>{{ link.label }}</span>
      </RouterLink>
    </nav>

    <!-- Mobile -->
    <div class="mobile-navbar">
      <button
        type="button"
        class="icon-button menu-button"
        :class="{ 'menu-button-open': isMobileMenuOpen }"
        :aria-expanded="isMobileMenuOpen"
        aria-label="Menu de navigation"
        @click="toggleMobileMenu"
      >
        <span class="menu-line menu-line-top" />
        <span class="menu-line menu-line-middle" />
        <span class="menu-line menu-line-bottom" />
      </button>
    </div>

    <!-- Menu mobile -->
    <Transition name="mobile-menu">
      <nav v-if="isMobileMenuOpen" class="mobile-nav">
        <RouterLink
          v-for="link in links"
          :key="link.to"
          :to="link.to"
          class="mobile-nav-link"
          :exact-active-class="link.to === '/' ? 'mobile-nav-link-active' : undefined"
          active-class="mobile-nav-link-active"
        >
          <component :is="link.icon" :size="18" />
          <span>{{ link.label }}</span>
        </RouterLink>
      </nav>
    </Transition>
  </div>
</template>
