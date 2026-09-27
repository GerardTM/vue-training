<script setup lang="ts">
import type { Component } from 'vue'

interface Props {
  title: string
  description?: string
  icon?: Component
  contentClass?: string
  headerClass?: string
}

withDefaults(defineProps<Props>(), {
  description: undefined,
  icon: undefined,
  contentClass: '',
  headerClass: '',
})
</script>

<template>
  <section class="page-section">
    <!-- Header -->
    <header class="page-section__header" :class="headerClass">
      <div class="page-section__heading">
        <!-- Back -->
        <div v-if="$slots.back" class="page-section__back">
          <slot name="back" />
        </div>

        <!-- Icon -->
        <div v-if="icon" class="page-section__icon">
          <component :is="icon" :size="22" :stroke-width="2" />
        </div>

        <!-- Title -->
        <div class="min-w-0">
          <h1 class="page-section__title">
            {{ title }}
          </h1>

          <p v-if="description" class="page-section__description">
            {{ description }}
          </p>
        </div>
      </div>

      <!-- Actions -->
      <div v-if="$slots.actions" class="page-section__actions">
        <slot name="actions" />
      </div>
    </header>

    <!-- Content -->
    <div class="page-section__content" :class="contentClass">
      <slot />
    </div>
  </section>
</template>
