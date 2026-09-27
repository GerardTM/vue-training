<script setup lang="ts">
import { FileText } from 'lucide-vue-next'

import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import RecordStatusBadge from '@/components/ui/RecordStatusBadge.vue'
import Section from '@/components/ui/Section.vue'
import Table from '@/components/ui/Table.vue'
import { RouteName } from '@/constants/RouteName'
import { useRouter } from 'vue-router'

const router = useRouter()

const columns = [
  {
    key: 'reference',
    label: 'Référence',
    sortable: true,
  },
  {
    key: 'name',
    label: 'Article',
    sortable: true,
  },
  {
    key: 'category',
    label: 'Catégorie',
    sortable: true,
  },
  {
    key: 'status',
    label: 'Statut',
    sortable: true,
  },
]

const products = [
  {
    id: 1,
    reference: 'ART-001',
    name: 'Article exemple 1',
    category: 'Catégorie A',
    status: 'active',
  },
  {
    id: 2,
    reference: 'ART-002',
    name: 'Article exemple 2',
    category: 'Catégorie B',
    status: 'inactive',
  },
  {
    id: 3,
    reference: 'ART-003',
    name: 'Article exemple 3',
    category: 'Catégorie A',
    status: 'active',
  },
]

const handleSelected = (items: unknown[]) => {
  console.log('Sélectionnés :', items)
}
</script>

<template>
  <Section title="Articles" description="Consultez et gérez les articles." :icon="FileText">
    <template #actions>
      <Button> Ajouter </Button>
    </template>
    <Card>
      <Table :columns="columns" :items="products" selectable @update:selected="handleSelected">
        <template #cell-status="{ value }">
          <RecordStatusBadge :status="value as 'active' | 'inactive'" />
        </template>

        <template #actions="{ item }">
          <div class="flex justify-end gap-1">
            <Button
              size="sm"
              variant="ghost"
              @click="
                router.push({
                  name: RouteName.PRODUCT_DETAIL,
                  params: { id: item.id as string },
                })
              "
            >
              Modifier
            </Button>

            <Button size="sm" variant="danger" @click="() => console.log('Supprimer', item)">
              Supprimer
            </Button>
          </div>
        </template>
      </Table>
    </Card>
  </Section>
</template>
