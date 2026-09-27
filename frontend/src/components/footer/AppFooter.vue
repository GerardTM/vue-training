<script setup lang="ts">
import { Heart } from 'lucide-vue-next'

const appName = 'SILL 2.0'
const currentYear = new Date().getFullYear()
</script>

<template>
  <footer class="footer">
    <div class="footer__content">
      <span> © {{ currentYear }} {{ appName }} </span>

      <span class="flex items-center gap-1">
        Fait avec
        <Heart :size="13" fill="currentColor" class="text-brand-500" />
      </span>
    </div>
  </footer>
</template>
