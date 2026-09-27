<script setup lang="ts">
import { ArrowLeft, Camera, Save, Trash2, UserRound } from 'lucide-vue-next'
import { computed, reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import Input from '@/components/ui/Input.vue'
import Section from '@/components/ui/Section.vue'
import { RouteName } from '@/constants/RouteName'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const avatarInput = ref<HTMLInputElement | null>(null)

const maxAvatarSize = 2 * 1024 * 1024
const supportedAvatarTypes = ['image/jpeg', 'image/png', 'image/webp']

const form = reactive({
  firstName: '',
  lastName: '',
  email: '',
  avatar: null as string | null,
})

const isSaving = ref(false)
const feedback = ref<{ type: 'success' | 'error'; message: string } | null>(null)

watch(
  () => authStore.user,
  (user) => {
    if (!user) return

    form.firstName = user.firstName ?? ''
    form.lastName = user.lastName ?? ''
    form.email = user.email
    form.avatar = user.avatar
  },
  { immediate: true },
)

const displayName = computed(() => {
  const name = `${form.firstName.trim()} ${form.lastName.trim()}`.trim()
  return name || 'Mon profil'
})

const initials = computed(() => {
  const value = [form.firstName, form.lastName]
    .map((name) => name.trim().charAt(0))
    .join('')
    .toUpperCase()

  return value || 'U'
})

const isDirty = computed(() => {
  const user = authStore.user

  return Boolean(
    user &&
    (form.firstName !== (user.firstName ?? '') ||
      form.lastName !== (user.lastName ?? '') ||
      form.email !== user.email ||
      form.avatar !== user.avatar),
  )
})

const resetForm = () => {
  const user = authStore.user
  if (!user) return

  form.firstName = user.firstName ?? ''
  form.lastName = user.lastName ?? ''
  form.email = user.email
  form.avatar = user.avatar
  feedback.value = null
}

const readImage = (file: File) =>
  new Promise<string>((resolve, reject) => {
    const reader = new FileReader()

    reader.addEventListener('load', () => {
      if (typeof reader.result === 'string') {
        resolve(reader.result)
      } else {
        reject(new Error('Image illisible'))
      }
    })
    reader.addEventListener('error', () => reject(new Error('Image illisible')))
    reader.readAsDataURL(file)
  })

const handleAvatarChange = async (event: Event) => {
  const input = event.target
  if (!(input instanceof HTMLInputElement)) return

  const file = input.files?.[0]
  input.value = ''
  if (!file) return

  if (!supportedAvatarTypes.includes(file.type)) {
    feedback.value = { type: 'error', message: 'Choisissez une image PNG, JPEG ou WebP.' }
    return
  }

  if (file.size > maxAvatarSize) {
    feedback.value = { type: 'error', message: 'L’image ne doit pas dépasser 2 Mo.' }
    return
  }

  try {
    form.avatar = await readImage(file)
    feedback.value = null
  } catch {
    feedback.value = { type: 'error', message: 'Impossible de lire cette image.' }
  }
}

const removeAvatar = () => {
  form.avatar = null
  feedback.value = null
}

const saveProfile = async () => {
  feedback.value = null
  isSaving.value = true

  try {
    await authStore.updateProfile({
      firstName: form.firstName.trim() || null,
      lastName: form.lastName.trim() || null,
      email: form.email.trim(),
      avatar: form.avatar,
    })

    feedback.value = { type: 'success', message: 'Profil mis à jour.' }
  } catch {
    feedback.value = {
      type: 'error',
      message: 'La mise à jour a échoué. Veuillez réessayer.',
    }
  } finally {
    isSaving.value = false
  }
}
</script>

<template>
  <Section
    title="Mon profil"
    description="Gérez vos informations personnelles et celles de votre compte."
    :icon="UserRound"
  >
    <template #back>
      <Button
        type="button"
        variant="ghost"
        size="sm"
        aria-label="Retour à l’accueil"
        @click="router.push({ name: RouteName.HOME })"
      >
        <ArrowLeft :size="18" />
      </Button>
    </template>

    <Card padding="none" class="overflow-hidden">
      <form @submit.prevent="saveProfile">
        <div class="grid md:grid-cols-[13rem_minmax(0,1fr)] xl:grid-cols-[16rem_minmax(0,1fr)]">
          <aside
            class="flex flex-col items-center border-b border-border bg-surface-muted/40 p-5 text-center sm:p-6 md:border-b-0 md:border-r md:p-6 xl:p-8"
          >
            <button
              type="button"
              class="group relative flex h-24 w-24 shrink-0 items-center justify-center overflow-hidden rounded-full bg-brand-100 text-2xl font-semibold text-brand-700 transition-shadow duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-4 dark:bg-brand-100 dark:text-brand-300 dark:focus-visible:ring-offset-surface"
              aria-label="Modifier la photo de profil"
              :disabled="isSaving"
              @click="avatarInput?.click()"
            >
              <img
                v-if="form.avatar"
                :src="form.avatar"
                :alt="`Photo de ${displayName}`"
                class="h-full w-full object-cover"
              />
              <span v-else>{{ initials }}</span>

              <span
                aria-hidden="true"
                class="absolute inset-0 flex flex-col items-center justify-center gap-1 bg-black/55 text-white opacity-0 transition-opacity duration-200 group-hover:opacity-100 group-focus-visible:opacity-100"
              >
                <Camera :size="23" />
                <span class="text-xs font-medium">Modifier</span>
              </span>
              <span
                aria-hidden="true"
                class="pointer-events-none absolute bottom-0 right-0 flex h-8 w-8 items-center justify-center rounded-full border-2 border-surface bg-brand-600 text-white shadow-sm transition-opacity duration-200 group-hover:opacity-0"
              >
                <Camera :size="15" />
              </span>
            </button>

            <input
              ref="avatarInput"
              class="sr-only"
              type="file"
              accept="image/jpeg,image/png,image/webp"
              aria-label="Choisir une nouvelle photo de profil"
              @change="handleAvatarChange"
            />

            <div class="mt-4 flex justify-center">
              <Button
                v-if="form.avatar"
                type="button"
                size="sm"
                variant="ghost"
                :disabled="isSaving"
                aria-label="Retirer la photo de profil"
                title="Retirer la photo de profil"
                @click="removeAvatar"
              >
                <Trash2 :size="16" />
                Retirer la photo
              </Button>
            </div>
            <p class="mt-2 text-xs text-content-muted">PNG, JPEG ou WebP · 2 Mo maximum</p>

            <h2 class="mt-4 wrap-break-word text-lg font-semibold text-content">
              {{ displayName }}
            </h2>
            <p class="mt-1 break-all text-sm text-content-secondary">
              {{ form.email || 'Adresse e-mail non renseignée' }}
            </p>
            <p class="mt-6 text-xs leading-5 text-content-muted">
              Votre nom et votre adresse e-mail sont utilisés dans votre espace personnel.
            </p>
          </aside>

          <div class="min-w-0">
            <div class="border-b border-border px-5 py-5 sm:px-6 xl:px-8">
              <h2 class="text-base font-semibold text-content">Informations personnelles</h2>
              <p class="mt-1 text-sm text-content-secondary">
                Modifiez les informations associées à votre compte.
              </p>
            </div>

            <div class="grid gap-5 p-5 sm:grid-cols-2 sm:p-6 xl:p-8">
              <Input
                id="firstName"
                v-model="form.firstName"
                label="Prénom"
                name="firstName"
                autocomplete="given-name"
                placeholder="Votre prénom"
              />

              <Input
                id="lastName"
                v-model="form.lastName"
                label="Nom"
                name="lastName"
                autocomplete="family-name"
                placeholder="Votre nom"
              />

              <Input
                id="email"
                v-model="form.email"
                class="sm:col-span-2"
                label="Adresse e-mail"
                name="email"
                type="email"
                autocomplete="email"
                placeholder="vous@exemple.fr"
                required
              />
            </div>

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

              <div class="flex justify-end gap-2">
                <Button
                  type="button"
                  variant="outline"
                  :disabled="!isDirty || isSaving"
                  @click="resetForm"
                >
                  Annuler
                </Button>
                <Button type="submit" :loading="isSaving" :disabled="!isDirty">
                  <Save :size="16" />
                  Enregistrer
                </Button>
              </div>
            </div>
          </div>
        </div>
      </form>
    </Card>
  </Section>
</template>
