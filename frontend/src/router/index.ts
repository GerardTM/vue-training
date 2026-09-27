import Home from '@/components/home/Home.vue'
import Import from '@/components/import/Import.vue'
import Login from '@/components/login/Login.vue'
import UserCreate from '@/components/login/UserCreate.vue'
import Logs from '@/components/logs/Logs.vue'
import Product from '@/components/product/Product.vue'
import ProductDetail from '@/components/product/ProductDetail.vue'
import ProfileEdit from '@/components/profile/ProfileEdit.vue'
import Referentiel from '@/components/referentiel/Referentiel.vue'

import { RouteName } from '@/constants/RouteName'
import AppLayout from '@/layouts/AppLayout.vue'
import { useAuthStore } from '@/stores/auth'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      component: AppLayout,
      meta: {
        requiresAuth: true,
      },

      children: [
        {
          path: '',
          name: RouteName.HOME,
          component: Home,
        },

        {
          path: 'referentiel',
          name: RouteName.REFERENTIEL,
          component: Referentiel,
        },

        {
          path: 'referentiel/users/new',
          name: RouteName.USER_CREATE,
          component: UserCreate,
        },

        {
          path: 'import',
          name: RouteName.IMPORT,
          component: Import,
        },

        {
          path: 'product',
          name: RouteName.PRODUCT,
          component: Product,
        },

        {
          path: 'product/:id',
          name: RouteName.PRODUCT_DETAIL,
          component: ProductDetail,
        },

        {
          path: 'logs',
          name: RouteName.LOGS,
          component: Logs,
        },

        {
          path: 'profile',
          name: RouteName.PROFILE,
          component: ProfileEdit,
        },
      ],
    },

    {
      path: '/login',
      name: RouteName.LOGIN,
      component: Login,
    },
  ],
})

router.beforeEach((to) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return '/login'
  }

  if (to.path === '/login' && authStore.isAuthenticated) {
    return '/'
  }
})

export default router
