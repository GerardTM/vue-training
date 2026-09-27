<script setup lang="ts">
import { FileInput, Upload } from 'lucide-vue-next'

import Badge from '@/components/ui/Badge.vue'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import Section from '@/components/ui/Section.vue'
import Table from '@/components/ui/Table.vue'

const columns = [
  {
    key: 'file',
    label: 'Fichier',
    sortable: true,
  },
  {
    key: 'date',
    label: 'Date',
    sortable: true,
  },
  {
    key: 'user',
    label: 'Utilisateur',
    sortable: true,
  },
  {
    key: 'status',
    label: 'Statut',
    sortable: true,
  },
]

const imports = [
  {
    id: 1,
    file: 'articles.csv',
    date: '25/09/2026 10:32',
    user: 'Jean Dupont',
    status: 'success',
  },
  {
    id: 2,
    file: 'referentiel.csv',
    date: '25/09/2026 09:15',
    user: 'Marie Martin',
    status: 'success',
  },
  {
    id: 3,
    file: 'articles_ancien.csv',
    date: '24/09/2026 16:42',
    user: 'Jean Dupont',
    status: 'error',
  },
]

const handleSelected = (items: unknown[]) => {
  console.log('Sélectionnés :', items)
}
</script>

<template>
  <Section title="Imports" description="Importez et consultez vos fichiers." :icon="FileInput">
    <template #actions>
      <Button variant="outline"> Historique </Button>

      <Button> Importer </Button>
    </template>

    <div class="grid gap-6 lg:grid-cols-3">
      <Card class="p-6 lg:col-span-1">
        <div class="flex h-full flex-col items-center justify-center text-center">
          <div
            class="flex h-14 w-14 items-center justify-center rounded-xl bg-brand-50 text-brand-600 dark:bg-brand-100 dark:text-brand-400"
          >
            <Upload :size="26" />
          </div>

          <h2 class="mt-4 text-base font-semibold text-content">Importer un fichier</h2>

          <p class="mt-2 text-sm leading-6 text-content-secondary">
            Sélectionnez un fichier CSV ou Excel à importer.
          </p>

          <Button class="mt-5"> Sélectionner un fichier </Button>
        </div>
      </Card>

      <Card class="lg:col-span-2">
        <Table :columns="columns" :items="imports" selectable @update:selected="handleSelected">
          <template #cell-status="{ value }">
            <Badge :variant="value === 'success' ? 'success' : 'danger'">
              {{ value === 'success' ? 'Terminé' : 'Échec' }}
            </Badge>
          </template>

          <template #actions="{ item }">
            <Button size="sm" variant="ghost" @click="() => console.log('Voir', item)">
              Voir
            </Button>
          </template>
        </Table>
      </Card>
    </div>
  </Section>
</template>
