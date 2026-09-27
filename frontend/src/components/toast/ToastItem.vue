<script setup lang="ts">
import { useToastStore, type Toast } from '@/stores/toastStore'
import { CheckCircle, CircleAlert, Info, TriangleAlert, X } from 'lucide-vue-next'
import { computed } from 'vue'

const props = defineProps<{
  toast: Toast
}>()

const toastStore = useToastStore()

const icon = computed(() => {
  switch (props.toast.type) {
    case 'success':
      return CheckCircle
    case 'error':
      return CircleAlert
    case 'warning':
      return TriangleAlert
    case 'info':
      return Info
  }
})

const iconClass = computed(() => {
  switch (props.toast.type) {
    case 'success':
      return 'text-green-500'
    case 'error':
      return 'text-red-500'
    case 'warning':
      return 'text-yellow-500'
    case 'info':
      return 'text-blue-500'
  }
})
</script>

<template>
  <div
    class="flex items-start gap-3 rounded-xl border border-border bg-surface p-4 shadow-elevated"
  >
    <component :is="icon" :size="20" class="mt-0.5 shrink-0" :class="iconClass" />

    <div class="min-w-0 flex-1">
      <p class="font-medium text-content">
        {{ toast.title }}
      </p>

      <p v-if="toast.message" class="mt-1 text-sm text-content-secondary">
        {{ toast.message }}
      </p>
    </div>

    <button
      type="button"
      class="shrink-0 text-content-muted transition-colors hover:text-content"
      aria-label="Fermer"
      @click="toastStore.remove(toast.id)"
    >
      <X :size="16" />
    </button>
  </div>
</template>
