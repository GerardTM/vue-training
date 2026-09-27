<script setup lang="ts">
import AppFooter from '@/components/footer/AppFooter.vue'
import AppHeader from '@/components/header/AppHeader.vue'
import ToastContainer from '@/components/toast/ToastContainer.vue'
</script>

<template>
  <div class="flex h-dvh flex-col overflow-hidden bg-background text-content">
    <AppHeader />

    <main class="min-h-0 flex-1 overflow-y-auto">
      <div class="mx-auto w-full max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <RouterView />
      </div>
    </main>

    <AppFooter />

    <ToastContainer />
  </div>
</template>
