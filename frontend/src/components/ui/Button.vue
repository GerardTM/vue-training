<script setup lang="ts">
import type { ButtonHTMLAttributes } from 'vue'

type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'

type ButtonSize = 'sm' | 'md' | 'lg'

interface Props extends /* @vue-ignore */ ButtonHTMLAttributes {
  type?: 'button' | 'submit' | 'reset'
  variant?: ButtonVariant
  size?: ButtonSize
  loading?: boolean
  disabled?: boolean
}

withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  loading: false,
  disabled: false,
})
</script>

<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="[
      'inline-flex items-center justify-center gap-2',
      'font-medium transition-all duration-200',
      'focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2',
      'dark:focus:ring-offset-surface',
      'disabled:cursor-not-allowed disabled:opacity-50',
      'cursor-pointer',

      {
        'rounded-md px-3 py-1.5 text-sm': size === 'sm',
        'rounded-md px-4 py-2 text-sm': size === 'md',
        'rounded-lg px-5 py-2.5 text-base': size === 'lg',
      },

      {
        'bg-brand-600 text-white hover:bg-brand-700': variant === 'primary',

        'bg-surface-muted text-content hover:bg-border': variant === 'secondary',

        'border border-border bg-surface text-content hover:bg-surface-muted':
          variant === 'outline',

        'text-content-secondary hover:bg-surface-muted hover:text-content': variant === 'ghost',

        'bg-red-600 text-white hover:bg-red-700': variant === 'danger',
      },
    ]"
  >
    <span
      v-if="loading"
      class="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent"
    />

    <slot v-else />
  </button>
</template>
