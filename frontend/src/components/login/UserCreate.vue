<script setup lang="ts">
import { ArrowLeft, Check, UserPlus } from 'lucide-vue-next'
import { computed, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import Input from '@/components/ui/Input.vue'
import Section from '@/components/ui/Section.vue'
import { RouteName } from '@/constants/RouteName'
import { userService } from '@/services/userService'
import type { UserCreatePayload } from '@/types/User'

const router = useRouter()

const form = reactive<UserCreatePayload & { passwordConfirmation: string }>({
  firstName: '',
  lastName: '',
  email: '',
  role: 'user',
  password: '',
  passwordConfirmation: '',
})

const isSaving = ref(false)
const isCreated = ref(false)
const feedback = ref<{ type: 'success' | 'error'; message: string } | null>(null)

const initials = computed(() => {
  const value = `${form.firstName.trim().charAt(0)}${form.lastName.trim().charAt(0)}`
    .toUpperCase()
    .trim()

  return value || 'U'
})

const createUser = async () => {
  if (isSaving.value || isCreated.value) return

  feedback.value = null

  if (form.password.length < 8) {
    feedback.value = {
      type: 'error',
      message: 'Le mot de passe doit contenir au moins 8 caractères.',
    }
    return
  }

  if (form.password !== form.passwordConfirmation) {
    feedback.value = { type: 'error', message: 'Les mots de passe ne correspondent pas.' }
    return
  }

  isSaving.value = true

  try {
    await userService.create({
      firstName: form.firstName.trim(),
      lastName: form.lastName.trim(),
      email: form.email.trim(),
      role: form.role,
      password: form.password,
    })

    isCreated.value = true
    feedback.value = { type: 'success', message: 'Le compte utilisateur a été créé.' }
  } catch {
    feedback.value = {
      type: 'error',
      message: 'La création a échoué. Vérifiez les informations et réessayez.',
    }
  } finally {
    isSaving.value = false
  }
}
</script>

<template>
  <Section
    title="Nouvel utilisateur"
    description="Créez un compte et définissez ses accès à l’application."
    :icon="UserPlus"
  >
    <template #back>
      <Button
        type="button"
        variant="ghost"
        size="sm"
        aria-label="Retour au référentiel"
        @click="router.push({ name: RouteName.REFERENTIEL })"
      >
        <ArrowLeft :size="18" />
      </Button>
    </template>

    <Card padding="none" class="overflow-hidden">
      <form @submit.prevent="createUser">
        <div class="grid md:grid-cols-[13rem_minmax(0,1fr)] xl:grid-cols-[16rem_minmax(0,1fr)]">
          <aside
            class="flex flex-col items-center border-b border-border bg-surface-muted/40 p-5 text-center sm:p-6 md:border-b-0 md:border-r md:p-6 xl:p-8"
          >
            <div
              class="flex h-20 w-20 items-center justify-center rounded-full bg-brand-100 text-xl font-semibold text-brand-700 dark:text-brand-300"
            >
              {{ initials }}
            </div>
            <h2 class="mt-4 wrap-break-word text-lg font-semibold text-content">
              {{
                form.firstName || form.lastName
                  ? `${form.firstName} ${form.lastName}`.trim()
                  : 'Nouveau compte'
              }}
            </h2>
            <p class="mt-1 break-all text-sm text-content-secondary">
              {{ form.email || 'Adresse e-mail du compte' }}
            </p>
            <p class="mt-6 text-xs leading-5 text-content-muted">
              Les champs marqués d’un astérisque sont obligatoires.
            </p>
          </aside>

          <div class="min-w-0">
            <div class="border-b border-border px-5 py-5 sm:px-6 xl:px-8">
              <h2 class="text-base font-semibold text-content">Informations du compte</h2>
              <p class="mt-1 text-sm text-content-secondary">
                Les identifiants initiaux pourront être modifiés par l’utilisateur après sa
                connexion.
              </p>
            </div>

            <fieldset
              :disabled="isSaving || isCreated"
              class="grid gap-5 p-5 sm:grid-cols-2 sm:p-6 xl:p-8"
            >
              <Input
                id="firstName"
                v-model="form.firstName"
                label="Prénom"
                name="firstName"
                autocomplete="given-name"
                placeholder="Prénom"
                required
              />

              <Input
                id="lastName"
                v-model="form.lastName"
                label="Nom"
                name="lastName"
                autocomplete="family-name"
                placeholder="Nom"
                required
              />

              <Input
                id="email"
                v-model="form.email"
                class="sm:col-span-2"
                label="Adresse e-mail"
                name="email"
                type="email"
                autocomplete="email"
                placeholder="nom@exemple.fr"
                required
              />

              <div class="space-y-2">
                <label for="role" class="block text-sm font-medium text-content">Rôle</label>
                <select id="role" v-model="form.role" name="role" class="input">
                  <option value="user">Utilisateur</option>
                  <option value="admin">Administrateur</option>
                </select>
              </div>

              <div class="hidden sm:block" aria-hidden="true" />

              <Input
                id="password"
                v-model="form.password"
                label="Mot de passe initial"
                name="password"
                type="password"
                autocomplete="new-password"
                placeholder="8 caractères minimum"
                hint="Au moins 8 caractères."
                required
              />

              <Input
                id="passwordConfirmation"
                v-model="form.passwordConfirmation"
                label="Confirmer le mot de passe"
                name="passwordConfirmation"
                type="password"
                autocomplete="new-password"
                placeholder="Saisissez-le à nouveau"
                required
              />
            </fieldset>

            <div
              class="flex flex-col gap-4 border-t border-border px-5 py-5 sm:flex-row sm:items-center sm:justify-between sm:px-6 xl:px-8"
            >
              <p
                v-if="feedback"
                :role="feedback.type === 'error' ? 'alert' : 'status'"
                :class="
                  feedback.type === 'error'
                    ? 'text-sm text-red-600'
                    : 'text-sm text-green-700 dark:text-green-400'
                "
              >
                {{ feedback.message }}
              </p>
              <span v-else />

              <div class="flex flex-wrap justify-end gap-2">
                <Button
                  v-if="!isCreated"
                  type="button"
                  variant="outline"
                  :disabled="isSaving"
                  @click="router.push({ name: RouteName.REFERENTIEL })"
                >
                  Annuler
                </Button>
                <Button v-if="!isCreated" type="submit" :loading="isSaving">
                  <UserPlus :size="16" />
                  Créer l’utilisateur
                </Button>
                <Button v-else type="button" @click="router.push({ name: RouteName.REFERENTIEL })">
                  <Check :size="16" />
                  Retour au référentiel
                </Button>
              </div>
            </div>
          </div>
        </div>
      </form>
    </Card>
  </Section>
</template>
