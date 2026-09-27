<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  modelValue?: string
  label?: string
  placeholder?: string
  type?: string
  name?: string
  id?: string
  error?: string
  hint?: string
  disabled?: boolean
  required?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  type: 'text',
  disabled: false,
  required: false,
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const inputId = computed(() => props.id || props.name)
</script>

<template>
  <div class="space-y-2">
    <label v-if="label" :for="inputId" class="block text-sm font-medium text-content">
      {{ label }}

      <span v-if="required" class="ml-1 text-brand-500"> * </span>
    </label>

    <input
      :id="inputId"
      :name="name"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :required="required"
      :class="[
        'input',
        'transition-colors duration-200',

        error ? 'border-red-500 focus:border-red-500 focus:ring-red-500' : '',
      ]"
      @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />

    <p v-if="error" class="text-sm text-red-500">
      {{ error }}
    </p>

    <p v-else-if="hint" class="text-sm text-content-muted">
      {{ hint }}
    </p>
  </div>
</template>
