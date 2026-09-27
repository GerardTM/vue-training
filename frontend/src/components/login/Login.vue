<script setup lang="ts">
import { authService } from '@/services/authService'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/themeStore'

import axios from 'axios'
import { Moon, Sun } from 'lucide-vue-next'
import { Field, Form } from 'vee-validate'
import { ref } from 'vue'
import * as yup from 'yup'

import { RouteName } from '@/constants/RouteName.ts'
import { useRouter } from 'vue-router'
import Button from '../ui/Button.vue'
import Card from '../ui/Card.vue'
import Input from '../ui/Input.vue'

const themeStore = useThemeStore()
const authStore = useAuthStore()
const router = useRouter()

const loading = ref(false)
const errorMessage = ref<string | null>(null)

const validationSchema = yup.object({
  email: yup
    .string()
    .required("L'adresse e-mail est requise")
    .email("L'adresse e-mail n'est pas valide"),

  password: yup.string().required('Le mot de passe est requis'),

  remember: yup.boolean(),
})

const handleLogin = async (values: Record<string, unknown>) => {
  const email = values.email
  const password = values.password

  if (typeof email !== 'string' || typeof password !== 'string') {
    errorMessage.value = 'Les identifiants ne sont pas valides'
    return
  }

  errorMessage.value = null
  loading.value = true

  try {
    const response = await authService.login(email, password)

    authStore.login(response.token, response.user)

    await router.push({ name: RouteName.HOME })
  } catch (error) {
    console.log('Erreur login :', error)

    if (axios.isAxiosError(error)) {
      console.log('Status :', error.response?.status)
      console.log('Data :', error.response?.data)

      errorMessage.value =
        error.response?.data?.error ??
        error.response?.data?.message ??
        'Email ou mot de passe incorrect'
    } else {
      errorMessage.value = 'Une erreur est survenue'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="relative flex min-h-dvh items-center justify-center bg-background px-4 py-8">
    <!-- Dark mode -->
    <Button
      type="button"
      variant="outline"
      size="sm"
      class="absolute right-4 top-4 h-10 w-10 rounded-xl p-0"
      :aria-label="themeStore.isDark ? 'Activer le mode clair' : 'Activer le mode sombre'"
      @click="themeStore.toggleDarkMode"
    >
      <Transition name="theme-icon" mode="out-in">
        <Sun v-if="themeStore.isDark" :key="'sun'" :size="19" />

        <Moon v-else :key="'moon'" :size="19" />
      </Transition>
    </Button>

    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="mb-8 text-center">
        <div
          class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-brand-600 text-white shadow-soft"
        >
          <span class="text-lg font-bold"> A </span>
        </div>

        <h1 class="text-2xl font-bold tracking-tight text-content">Bienvenue</h1>

        <p class="mt-2 text-sm text-content-secondary">Connectez-vous à votre compte</p>
      </div>

      <!-- Login -->
      <Card>
        <Form
          :validation-schema="validationSchema"
          :initial-values="{
            email: '',
            password: '',
            remember: false,
          }"
          class="space-y-5"
          @submit="handleLogin"
        >
          <!-- Email -->
          <Field v-slot="{ value, handleChange, errorMessage: fieldError }" name="email">
            <Input
              :model-value="value"
              label="Adresse e-mail"
              placeholder="vous@exemple.com"
              name="email"
              type="email"
              id="email"
              autocomplete="email"
              :error="fieldError"
              required
              @update:model-value="handleChange"
            />
          </Field>

          <!-- Password -->
          <Field v-slot="{ value, handleChange, errorMessage: fieldError }" name="password">
            <div>
              <div class="mb-2 flex items-center justify-between">
                <label for="password" class="text-sm font-medium text-content">
                  Mot de passe
                </label>

                <RouterLink
                  to="/forgot-password"
                  class="text-sm font-medium text-brand-600 hover:text-brand-700 dark:text-brand-400 dark:hover:text-brand-300"
                >
                  Mot de passe oublié ?
                </RouterLink>
              </div>

              <Input
                :model-value="value"
                name="password"
                id="password"
                type="password"
                autocomplete="current-password"
                placeholder="••••••••"
                :error="fieldError"
                required
                @update:model-value="handleChange"
              />
            </div>
          </Field>

          <!-- Remember -->
          <Field v-slot="{ value, handleChange }" name="remember">
            <div class="flex items-center gap-2">
              <input
                id="remember"
                type="checkbox"
                name="remember"
                :checked="value"
                class="h-4 w-4 rounded border-border accent-brand-600"
                @change="handleChange"
              />

              <label for="remember" class="text-sm text-content-secondary">
                Se souvenir de moi
              </label>
            </div>
          </Field>

          <!-- Server error -->
          <div
            v-if="errorMessage"
            class="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-600 dark:border-red-900/50 dark:bg-red-950/30 dark:text-red-400"
            role="alert"
          >
            {{ errorMessage }}
          </div>

          <!-- Submit -->
          <Button type="submit" variant="primary" size="md" :loading="loading" class="w-full">
            Se connecter
          </Button>
        </Form>

        <!-- Register -->
        <div class="mt-6 border-t border-border pt-6 text-center">
          <p class="text-sm text-content-secondary">
            Vous n'avez pas encore de compte ?

            <RouterLink
              to="/register"
              class="font-medium text-brand-600 hover:text-brand-700 dark:text-brand-400 dark:hover:text-brand-300"
            >
              Créer un compte
            </RouterLink>
          </p>
        </div>
      </Card>

      <!-- Footer -->
      <p class="mt-6 text-center text-xs text-content-muted">
        © {{ new Date().getFullYear() }} MonApp. Tous droits réservés.
      </p>
    </div>
  </main>
</template>
```
