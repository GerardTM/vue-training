```vue
<script setup lang="ts">
import {
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  ChevronUp,
  ChevronsUpDown,
  LoaderCircle,
  Search,
} from 'lucide-vue-next'
import { computed, ref } from 'vue'

export interface TableColumn {
  key: string
  label: string
  sortable?: boolean
  searchable?: boolean
  align?: 'left' | 'center' | 'right'
  width?: string
}

interface Props {
  columns: TableColumn[]
  items: Record<string, unknown>[]

  loading?: boolean

  searchable?: boolean
  searchPlaceholder?: string

  pagination?: boolean
  pageSize?: number
  pageSizeOptions?: number[]

  selectable?: boolean

  emptyMessage?: string
  rowKey?: string
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,

  searchable: true,
  searchPlaceholder: 'Rechercher...',

  pagination: true,
  pageSize: 10,
  pageSizeOptions: () => [5, 10, 25, 50],

  selectable: false,

  emptyMessage: 'Aucun résultat',
  rowKey: 'id',
})

const emit = defineEmits<{
  'update:selected': [items: Record<string, unknown>[]]
}>()

/*
|--------------------------------------------------------------------------
| Recherche
|--------------------------------------------------------------------------
*/

const search = ref('')

const searchableColumns = computed(() => {
  return props.columns.filter((column) => column.searchable !== false)
})

const filteredItems = computed(() => {
  if (!search.value.trim()) {
    return props.items
  }

  const query = search.value.toLowerCase().trim()

  return props.items.filter((item) => {
    return searchableColumns.value.some((column) => {
      const value = item[column.key]

      return String(value ?? '')
        .toLowerCase()
        .includes(query)
    })
  })
})

/*
|--------------------------------------------------------------------------
| Tri
|--------------------------------------------------------------------------
*/

const sortKey = ref<string | null>(null)
const sortDirection = ref<'asc' | 'desc'>('asc')

const sortedItems = computed(() => {
  const currentSortKey = sortKey.value

  if (currentSortKey === null) {
    return filteredItems.value
  }

  const items = [...filteredItems.value]

  items.sort((a, b) => {
    const aValue = a[currentSortKey]
    const bValue = b[currentSortKey]

    if (aValue == null) return 1
    if (bValue == null) return -1

    const aString = String(aValue).toLowerCase()
    const bString = String(bValue).toLowerCase()

    let comparison = 0

    if (typeof aValue === 'number' && typeof bValue === 'number') {
      comparison = aValue - bValue
    } else {
      comparison = aString.localeCompare(bString, undefined, {
        numeric: true,
      })
    }

    return sortDirection.value === 'asc' ? comparison : -comparison
  })

  return items
})

const toggleSort = (column: TableColumn) => {
  if (!column.sortable) {
    return
  }

  if (sortKey.value === column.key) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'

    return
  }

  sortKey.value = column.key
  sortDirection.value = 'asc'
}

/*
|--------------------------------------------------------------------------
| Pagination
|--------------------------------------------------------------------------
*/

const currentPage = ref(1)
const currentPageSize = ref(props.pageSize)

const totalPages = computed(() => {
  if (!props.pagination) {
    return 1
  }

  return Math.max(1, Math.ceil(sortedItems.value.length / currentPageSize.value))
})

const paginatedItems = computed(() => {
  if (!props.pagination) {
    return sortedItems.value
  }

  const start = (currentPage.value - 1) * currentPageSize.value

  const end = start + currentPageSize.value

  return sortedItems.value.slice(start, end)
})

const displayedPages = computed(() => {
  const pages: number[] = []

  const total = totalPages.value
  const current = currentPage.value

  if (total <= 5) {
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }

    return pages
  }

  pages.push(1)

  if (current > 3) {
    pages.push(-1)
  }

  const start = Math.max(2, current - 1)
  const end = Math.min(total - 1, current + 1)

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }

  if (current < total - 2) {
    pages.push(-1)
  }

  pages.push(total)

  return pages
})

const changePage = (page: number) => {
  if (page < 1 || page > totalPages.value) {
    return
  }

  currentPage.value = page
}

const changePageSize = () => {
  currentPage.value = 1
}

/*
|--------------------------------------------------------------------------
| Sélection
|--------------------------------------------------------------------------
*/

const selectedKeys = ref<Set<string | number>>(new Set())

const getRowKey = (item: Record<string, unknown>) => {
  return item[props.rowKey] as string | number
}

const isSelected = (item: Record<string, unknown>) => {
  return selectedKeys.value.has(getRowKey(item))
}

const toggleSelection = (item: Record<string, unknown>) => {
  const key = getRowKey(item)

  const next = new Set(selectedKeys.value)

  if (next.has(key)) {
    next.delete(key)
  } else {
    next.add(key)
  }

  selectedKeys.value = next

  emitSelected()
}

const allVisibleSelected = computed(() => {
  if (paginatedItems.value.length === 0) {
    return false
  }

  return paginatedItems.value.every((item) => selectedKeys.value.has(getRowKey(item)))
})

const toggleSelectAll = () => {
  const next = new Set(selectedKeys.value)

  if (allVisibleSelected.value) {
    paginatedItems.value.forEach((item) => {
      next.delete(getRowKey(item))
    })
  } else {
    paginatedItems.value.forEach((item) => {
      next.add(getRowKey(item))
    })
  }

  selectedKeys.value = next

  emitSelected()
}

const selectedItems = computed(() => {
  return props.items.filter((item) => selectedKeys.value.has(getRowKey(item)))
})

const emitSelected = () => {
  emit('update:selected', selectedItems.value)
}

/*
|--------------------------------------------------------------------------
| Informations pagination
|--------------------------------------------------------------------------
*/

const firstItem = computed(() => {
  if (sortedItems.value.length === 0) {
    return 0
  }

  return (currentPage.value - 1) * currentPageSize.value + 1
})

const lastItem = computed(() => {
  return Math.min(currentPage.value * currentPageSize.value, sortedItems.value.length)
})
</script>

<template>
  <div class="card overflow-hidden">
    <!-- Toolbar -->
    <div
      v-if="searchable || $slots.toolbar"
      class="flex flex-col gap-3 border-b border-border p-4 sm:flex-row sm:items-center sm:justify-between"
    >
      <!-- Search -->
      <div v-if="searchable" class="relative w-full sm:max-w-xs">
        <Search
          :size="17"
          class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-content-muted"
        />

        <input
          v-model="search"
          type="search"
          :placeholder="searchPlaceholder"
          class="input pl-9"
          @input="currentPage = 1"
        />
      </div>

      <!-- Custom toolbar -->
      <div v-if="$slots.toolbar" class="flex items-center gap-2">
        <slot name="toolbar" :selected="selectedItems" />
      </div>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto">
      <table class="w-full border-collapse">
        <!-- Header -->
        <thead>
          <tr class="border-b border-border bg-surface-muted">
            <!-- Select all -->
            <th v-if="selectable" class="w-12 px-4 py-3">
              <input
                type="checkbox"
                :checked="allVisibleSelected"
                class="h-4 w-4 rounded border-border accent-brand-600"
                @change="toggleSelectAll"
              />
            </th>

            <!-- Columns -->
            <th
              v-for="column in columns"
              :key="column.key"
              :style="{ width: column.width }"
              :class="[
                'px-4 py-3 text-xs font-semibold uppercase',
                'tracking-wider text-content-secondary',
                'select-none',

                {
                  'text-left': column.align === 'left' || !column.align,

                  'text-center': column.align === 'center',

                  'text-right': column.align === 'right',
                },
              ]"
            >
              <button
                v-if="column.sortable"
                type="button"
                class="inline-flex items-center gap-1.5 transition-colors hover:text-content"
                @click="toggleSort(column)"
              >
                {{ column.label }}

                <ChevronUp
                  v-if="sortKey === column.key && sortDirection === 'asc'"
                  :size="14"
                  class="text-brand-500"
                />

                <ChevronDown
                  v-else-if="sortKey === column.key && sortDirection === 'desc'"
                  :size="14"
                  class="text-brand-500"
                />

                <ChevronsUpDown v-else :size="14" class="text-content-muted" />
              </button>

              <span v-else>
                {{ column.label }}
              </span>
            </th>

            <!-- Actions -->
            <th
              v-if="$slots.actions"
              class="w-1 px-4 py-3 text-right text-xs font-semibold uppercase tracking-wider text-content-secondary"
            >
              Actions
            </th>
          </tr>
        </thead>

        <!-- Body -->
        <tbody class="divide-y divide-border">
          <!-- Loading -->
          <tr v-if="loading">
            <td
              :colspan="columns.length + (selectable ? 1 : 0) + ($slots.actions ? 1 : 0)"
              class="px-4 py-14"
            >
              <div class="flex flex-col items-center justify-center gap-3">
                <LoaderCircle :size="26" class="animate-spin text-brand-500" />

                <span class="text-sm text-content-muted"> Chargement... </span>
              </div>
            </td>
          </tr>

          <!-- Empty -->
          <tr v-else-if="paginatedItems.length === 0">
            <td
              :colspan="columns.length + (selectable ? 1 : 0) + ($slots.actions ? 1 : 0)"
              class="px-4 py-14 text-center"
            >
              <div class="flex flex-col items-center justify-center gap-2">
                <span class="text-sm font-medium text-content-secondary">
                  {{ search ? 'Aucun résultat pour cette recherche' : emptyMessage }}
                </span>

                <span v-if="search" class="text-xs text-content-muted">
                  Essayez avec un autre terme.
                </span>
              </div>
            </td>
          </tr>

          <!-- Rows -->
          <tr
            v-for="item in paginatedItems"
            v-else
            :key="String(getRowKey(item))"
            :class="[
              'group transition-colors',
              'hover:bg-surface-muted/60',

              {
                'bg-brand-50/50 dark:bg-brand-100/20': isSelected(item),
              },
            ]"
          >
            <!-- Selection -->
            <td v-if="selectable" class="w-12 px-4 py-3.5">
              <input
                type="checkbox"
                :checked="isSelected(item)"
                class="h-4 w-4 rounded border-border accent-brand-600"
                @change="toggleSelection(item)"
              />
            </td>

            <!-- Cells -->
            <td
              v-for="column in columns"
              :key="column.key"
              :class="[
                'px-4 py-3.5 text-sm text-content',

                {
                  'text-left': column.align === 'left' || !column.align,

                  'text-center': column.align === 'center',

                  'text-right': column.align === 'right',
                },
              ]"
            >
              <slot :name="`cell-${column.key}`" :item="item" :value="item[column.key]">
                {{ item[column.key] }}
              </slot>
            </td>

            <!-- Actions -->
            <td v-if="$slots.actions" class="px-4 py-3.5 text-right">
              <slot name="actions" :item="item" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Footer / Pagination -->
    <div
      v-if="pagination && sortedItems.length > 0"
      class="flex flex-col gap-3 border-t border-border px-3 py-3 sm:gap-4 sm:px-4 lg:flex-row lg:items-center lg:justify-between"
    >
      <!-- Information -->
      <div class="text-xs text-content-secondary sm:text-sm">
        Affichage de
        <span class="font-medium text-content">
          {{ firstItem }}
        </span>
        à
        <span class="font-medium text-content">
          {{ lastItem }}
        </span>
        sur
        <span class="font-medium text-content">
          {{ sortedItems.length }}
        </span>
        résultat{{ sortedItems.length > 1 ? 's' : '' }}
      </div>

      <div class="flex min-w-0 items-center justify-between gap-3 sm:justify-start">
        <!-- Page size -->
        <select
          v-model.number="currentPageSize"
          class="w-24 shrink-0 rounded-md border border-border bg-surface px-2.5 py-1.5 text-sm text-content focus:border-brand-500 focus:outline-none"
          @change="changePageSize"
        >
          <option v-for="size in pageSizeOptions" :key="size" :value="size">
            {{ size }} / page
          </option>
        </select>

        <!-- Pagination -->
        <div class="flex min-w-0 items-center justify-between gap-1 sm:justify-start">
          <!-- Previous -->
          <button
            type="button"
            :disabled="currentPage === 1"
            aria-label="Page précédente"
            class="flex h-9 w-9 shrink-0 items-center justify-center rounded-md border border-border text-sm text-content transition-colors hover:bg-surface-muted disabled:cursor-not-allowed disabled:opacity-40 sm:h-auto sm:w-auto sm:px-3 sm:py-1.5"
            @click="changePage(currentPage - 1)"
          >
            <ChevronLeft :size="16" class="sm:hidden" />
            <span class="sr-only sm:not-sr-only">Précédent</span>
          </button>

          <span class="px-1 text-sm text-content-secondary sm:hidden" aria-live="polite">
            {{ currentPage }} / {{ totalPages }}
          </span>

          <!-- Pages -->
          <template v-for="(page, index) in displayedPages" :key="`${page}-${index}`">
            <span v-if="page === -1" class="hidden px-1 text-content-muted sm:inline"> … </span>

            <button
              v-else
              type="button"
              :class="[
                'hidden min-w-9 rounded-md px-2.5 py-1.5 sm:inline-flex',
                'text-sm transition-colors',

                page === currentPage
                  ? 'bg-brand-600 text-white'
                  : 'text-content-secondary hover:bg-surface-muted',
              ]"
              @click="changePage(page)"
            >
              {{ page }}
            </button>
          </template>

          <!-- Next -->
          <button
            type="button"
            :disabled="currentPage === totalPages"
            aria-label="Page suivante"
            class="flex h-9 w-9 shrink-0 items-center justify-center rounded-md border border-border text-sm text-content transition-colors hover:bg-surface-muted disabled:cursor-not-allowed disabled:opacity-40 sm:h-auto sm:w-auto sm:px-3 sm:py-1.5"
            @click="changePage(currentPage + 1)"
          >
            <ChevronRight :size="16" class="sm:hidden" />
            <span class="sr-only sm:not-sr-only">Suivant</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
```
