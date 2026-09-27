import { defineStore } from 'pinia'
import { ref } from 'vue'

export type ToastType = 'success' | 'error' | 'warning' | 'info'

export interface Toast {
  id: number
  type: ToastType
  title: string
  message?: string
  duration: number
}

export const useToastStore = defineStore('toast', () => {
  const toasts = ref<Toast[]>([])

  let nextId = 0

  const remove = (id: number) => {
    toasts.value = toasts.value.filter((toast) => toast.id !== id)
  }

  const show = (title: string, type: ToastType = 'info', message?: string, duration = 4000) => {
    const id = nextId++

    toasts.value.push({
      id,
      type,
      title,
      message,
      duration,
    })

    if (duration > 0) {
      setTimeout(() => {
        remove(id)
      }, duration)
    }
  }

  const success = (title: string, message?: string, duration?: number) => {
    show(title, 'success', message, duration)
  }

  const error = (title: string, message?: string, duration?: number) => {
    show(title, 'error', message, duration)
  }

  const warning = (title: string, message?: string, duration?: number) => {
    show(title, 'warning', message, duration)
  }

  const info = (title: string, message?: string, duration?: number) => {
    show(title, 'info', message, duration)
  }

  const clear = () => {
    toasts.value = []
  }

  return {
    toasts,
    show,
    success,
    error,
    warning,
    info,
    remove,
    clear,
  }
})
