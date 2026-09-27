<script setup lang="ts">
defineProps<{
  name: string
}>()
</script>

<template>
  <RouterLink to="/" class="group flex items-center gap-2.5">
    <div class="logo">
      <span class="text-sm font-bold text-white">C</span>
    </div>

    <span class="text-lg font-semibold tracking-tight text-content">
      {{ name }}
    </span>
  </RouterLink>
</template>
