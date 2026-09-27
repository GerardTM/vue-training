<script setup lang="ts">
type BadgeVariant = 'default' | 'success' | 'warning' | 'danger' | 'info'

withDefaults(
  defineProps<{
    variant?: BadgeVariant
  }>(),
  {
    variant: 'default',
  },
)
</script>

<template>
  <span
    :class="[
      'inline-flex items-center rounded-full px-2.5 py-1',
      'text-xs font-medium',

      {
        'bg-surface-muted text-content-secondary': variant === 'default',

        'bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-400':
          variant === 'success',

        'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/40 dark:text-yellow-400':
          variant === 'warning',

        'bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-400': variant === 'danger',

        'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-400': variant === 'info',
      },
    ]"
  >
    <slot />
  </span>
</template>
