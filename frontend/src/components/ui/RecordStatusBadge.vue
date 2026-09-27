<script setup lang="ts">
import Badge from '@/components/ui/Badge.vue'

defineProps<{
  status: 'active' | 'inactive'
}>()
</script>

<template>
  <Badge :variant="status === 'active' ? 'success' : 'danger'">
    {{ status === 'active' ? 'Actif' : 'Inactif' }}
  </Badge>
</template>
