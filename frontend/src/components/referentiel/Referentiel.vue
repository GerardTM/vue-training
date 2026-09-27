<script setup lang="ts">
import { ClipboardList, UserPlus } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import RecordStatusBadge from '@/components/ui/RecordStatusBadge.vue'
import Section from '@/components/ui/Section.vue'
import Table from '@/components/ui/Table.vue'
import { RouteName } from '@/constants/RouteName'
import { useToastStore } from '@/stores/toastStore'

const router = useRouter()
const toast = useToastStore()

const columns = [
  {
    key: 'name',
    label: 'Nom',
    sortable: true,
  },
  {
    key: 'email',
    label: 'E-mail',
    sortable: true,
  },
  {
    key: 'role',
    label: 'Rôle',
    sortable: true,
  },
  {
    key: 'status',
    label: 'Statut',
    sortable: true,
    searchable: false,
  },
]

const users = [
  {
    id: 1,
    name: 'Jean Dupont',
    email: 'jean@example.com',
    role: 'Administrateur',
    status: 'active',
  },
  {
    id: 2,
    name: 'Marie Martin',
    email: 'marie@example.com',
    role: 'Utilisateur',
    status: 'inactive',
  },
]

const handleSelected = (users: unknown[]) => {
  console.log('Sélectionnés :', users)

  toast.info('', `${users.length} utilisateur(s) sélectionné(s)`)
}
</script>

<template>
  <Section
    title="Référentiel"
    description="Gérez les données du référentiel."
    :icon="ClipboardList"
  >
    <Card>
      <Table :columns="columns" :items="users" selectable @update:selected="handleSelected">
        <template #cell-status="{ value }">
          <RecordStatusBadge :status="value as 'active' | 'inactive'" />
        </template>

        <template #actions="{ item }">
          <div class="flex justify-end gap-1">
            <Button size="sm" variant="ghost" @click="() => console.log('Modifier', item)">
              Modifier
            </Button>

            <Button size="sm" variant="danger" @click="() => console.log('Supprimer', item)">
              Supprimer
            </Button>
          </div>
        </template>

        <template #toolbar>
          <Button @click="router.push({ name: RouteName.USER_CREATE })">
            <UserPlus :size="16" />
            Ajouter
          </Button>
        </template>
      </Table>
    </Card>
  </Section>
</template>
