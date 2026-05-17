import { defineStore } from 'pinia'

import api, { getApiError } from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('access_token') || '',
    user: null,
    loading: false,
    error: '',
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.token),
    isAdmin: (state) => state.user?.role === 'admin',
    isOrganizer: (state) => state.user?.role === 'organizer',
    isStudent: (state) => state.user?.role === 'student',
  },
  actions: {
    initFromStorage() {
      this.token = localStorage.getItem('access_token') || ''
    },
    async loginWithPassword(username, password) {
      this.loading = true
      this.error = ''
      try {
        const { data } = await api.post('/auth/login', { username, password })
        this.token = data.access_token
        localStorage.setItem('access_token', data.access_token)
        await this.fetchMe()
      } catch (error) {
        this.error = getApiError(error, 'Autentificare esuata')
        throw error
      } finally {
        this.loading = false
      }
    },
    async loginWithGoogleIdToken(idToken) {
      this.loading = true
      this.error = ''
      try {
        const { data } = await api.post('/auth/google', { id_token: idToken })
        this.token = data.access_token
        localStorage.setItem('access_token', data.access_token)
        await this.fetchMe()
      } catch (error) {
        this.error =
          getApiError(error, 'Autentificarea Google a esuat. Foloseste un cont @student.usv.ro') +
          (error?.response?.data?.detail ? ` (${error.response.data.detail})` : '')
        throw error
      } finally {
        this.loading = false
      }
    },
    async fetchMe() {
      if (!this.token) {
        this.user = null
        return null
      }
      try {
        const { data } = await api.get('/auth/me')
        this.user = data
        return data
      } catch (error) {
        this.logout()
        throw error
      }
    },
    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem('access_token')
    },
  },
})
