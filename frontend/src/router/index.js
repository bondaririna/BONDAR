import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '@/stores/auth'
import AdminValidationView from '@/views/AdminValidationView.vue'
import EventsView from '@/views/EventsView.vue'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import NewEventView from '@/views/NewEventView.vue'
import OrganizerEventsView from '@/views/OrganizerEventsView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/events', name: 'events', component: EventsView },
    {
      path: '/organizer/events',
      name: 'organizer-events',
      component: OrganizerEventsView,
      meta: { requiresAuth: true, roles: ['organizer', 'admin'] },
    },
    {
      path: '/organizer/new-event',
      name: 'new-event',
      component: NewEventView,
      meta: { requiresAuth: true, roles: ['organizer', 'admin'] },
    },
    {
      path: '/admin/validate',
      name: 'admin-validate',
      component: AdminValidationView,
      meta: { requiresAuth: true, roles: ['admin'] },
    },
  ],
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  auth.initFromStorage()

  if (auth.token && !auth.user) {
    try {
      await auth.fetchMe()
    } catch {
      if (to.path !== '/login') {
        return '/login'
      }
    }
  }

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return '/login'
  }

  if (to.meta.roles && !to.meta.roles.includes(auth.user?.role || '')) {
    return '/events'
  }

  return true
})

export default router
