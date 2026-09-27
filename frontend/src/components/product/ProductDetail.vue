<script setup lang="ts">
import { ArrowLeft, FileText } from 'lucide-vue-next'
import { useRoute, useRouter } from 'vue-router'

import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import Section from '@/components/ui/Section.vue'
import { RouteName } from '@/constants/RouteName'

const route = useRoute()
const router = useRouter()

const productId = Number(route.params.id)

const goBack = () => {
  router.push({ name: RouteName.PRODUCT })
}
</script>

<template>
  <Section
    title="Détail de l'article"
    description="Consultez et modifiez les informations de l'article."
    :icon="FileText"
  >
    <template #back>
      <Button variant="ghost" size="sm" @click="goBack">
        <ArrowLeft :size="18" />
      </Button>
    </template>

    <Card class="p-6">
      <p class="text-sm text-content-secondary">ID de l'article</p>

      <p class="mt-1 text-lg font-semibold text-content">
        {{ productId }}
      </p>
    </Card>
  </Section>
</template>
