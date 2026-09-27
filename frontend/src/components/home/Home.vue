<script setup lang="ts">
import {
  Activity,
  ArrowRight,
  ClipboardList,
  FileInput,
  FileText,
  ScrollText,
} from 'lucide-vue-next'

import Badge from '@/components/ui/Badge.vue'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import Section from '@/components/ui/Section.vue'
</script>

<template>
  <Section title="Accueil" description="Bienvenue sur SILL 2.0." :icon="Activity">
    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <Card class="p-5">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-content-secondary">Utilisateurs</p>

            <p class="mt-2 text-2xl font-bold text-content">24</p>
          </div>

          <div
            class="flex h-10 w-10 items-center justify-center rounded-lg bg-brand-50 text-brand-600 dark:bg-brand-100 dark:text-brand-400"
          >
            <ClipboardList :size="20" />
          </div>
        </div>
      </Card>

      <Card class="p-5">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-content-secondary">Articles</p>

            <p class="mt-2 text-2xl font-bold text-content">1 248</p>
          </div>

          <div
            class="flex h-10 w-10 items-center justify-center rounded-lg bg-brand-50 text-brand-600 dark:bg-brand-100 dark:text-brand-400"
          >
            <FileText :size="20" />
          </div>
        </div>
      </Card>

      <Card class="p-5">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-content-secondary">Imports</p>

            <p class="mt-2 text-2xl font-bold text-content">86</p>
          </div>

          <div
            class="flex h-10 w-10 items-center justify-center rounded-lg bg-brand-50 text-brand-600 dark:bg-brand-100 dark:text-brand-400"
          >
            <FileInput :size="20" />
          </div>
        </div>
      </Card>

      <Card class="p-5">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-content-secondary">Logs aujourd'hui</p>

            <p class="mt-2 text-2xl font-bold text-content">342</p>
          </div>

          <div
            class="flex h-10 w-10 items-center justify-center rounded-lg bg-brand-50 text-brand-600 dark:bg-brand-100 dark:text-brand-400"
          >
            <ScrollText :size="20" />
          </div>
        </div>
      </Card>
    </div>

    <div class="mt-6 grid gap-6 lg:grid-cols-2">
      <Card class="p-4 sm:p-6">
        <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 class="text-base font-semibold text-content">Activité récente</h2>

            <p class="mt-1 text-sm text-content-secondary">Les dernières actions effectuées.</p>
          </div>

          <Button variant="ghost" size="sm" class="self-start sm:self-auto">
            Voir tout
            <ArrowRight :size="16" />
          </Button>
        </div>

        <div class="mt-6 space-y-4">
          <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
            <div class="min-w-0">
              <p class="text-sm font-medium text-content">Import des articles</p>

              <p class="text-xs text-content-muted">Il y a 10 minutes</p>
            </div>

            <Badge variant="success" class="self-start sm:self-auto"> Terminé </Badge>
          </div>

          <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
            <div class="min-w-0">
              <p class="text-sm font-medium text-content">Modification utilisateur</p>

              <p class="text-xs text-content-muted">Il y a 25 minutes</p>
            </div>

            <Badge variant="success" class="self-start sm:self-auto"> Terminé </Badge>
          </div>

          <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
            <div class="min-w-0">
              <p class="text-sm font-medium text-content">Import référentiel</p>

              <p class="text-xs text-content-muted">Il y a 1 heure</p>
            </div>

            <Badge variant="danger" class="self-start sm:self-auto"> Échec </Badge>
          </div>
        </div>
      </Card>

      <Card class="p-4 sm:p-6">
        <h2 class="text-base font-semibold text-content">Accès rapides</h2>

        <p class="mt-1 text-sm text-content-secondary">
          Accédez rapidement aux principales fonctionnalités.
        </p>

        <div class="mt-6 grid gap-3 sm:grid-cols-2">
          <Button variant="outline">
            <ClipboardList :size="17" />
            Référentiel
          </Button>

          <Button variant="outline">
            <FileInput :size="17" />
            Nouvel import
          </Button>

          <Button variant="outline">
            <FileText :size="17" />
            Articles
          </Button>

          <Button variant="outline">
            <ScrollText :size="17" />
            Consulter les logs
          </Button>
        </div>
      </Card>
    </div>
  </Section>
</template>
