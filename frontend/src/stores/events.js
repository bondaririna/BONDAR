import { defineStore } from 'pinia'

import api, { getApiError } from '@/services/api'

export const useEventsStore = defineStore('events', {
  state: () => ({
    items: [],
    selected: null,
    loading: false,
    error: '',
    message: '',
  }),
  actions: {
    async fetchEvents(params = {}) {
      this.loading = true
      this.error = ''
      try {
        const { data } = await api.get('/events', { params })
        this.items = data
        return data
      } catch (error) {
        this.error = getApiError(error, 'Nu pot incarca evenimentele')
        throw error
      } finally {
        this.loading = false
      }
    },
    async fetchEvent(eventId) {
      this.loading = true
      this.error = ''
      try {
        const { data } = await api.get(`/events/${eventId}`)
        this.selected = data
        return data
      } catch (error) {
        this.error = getApiError(error, 'Nu pot incarca evenimentul')
        throw error
      } finally {
        this.loading = false
      }
    },
    async createEvent(payload) {
      this.error = ''
      this.loading = true
      try {
        const { data } = await api.post('/events', payload)
        this.message = 'Eveniment creat cu succes.'
        return data
      } catch (error) {
        this.error = getApiError(error, 'Nu pot crea evenimentul')
        throw error
      } finally {
        this.loading = false
      }
    },
    async updateEvent(eventId, payload) {
      this.error = ''
      this.loading = true
      try {
        const { data } = await api.patch(`/events/${eventId}`, payload)
        this.message = 'Eveniment actualizat.'
        return data
      } catch (error) {
        this.error = getApiError(error, 'Nu pot actualiza evenimentul')
        throw error
      } finally {
        this.loading = false
      }
    },
    async deleteEvent(eventId) {
      this.error = ''
      this.loading = true
      try {
        await api.delete(`/events/${eventId}`)
        this.message = 'Eveniment sters.'
      } catch (error) {
        this.error = getApiError(error, 'Nu pot sterge evenimentul')
        throw error
      } finally {
        this.loading = false
      }
    },
    async validateEvent(eventId, status) {
      this.error = ''
      try {
        const { data } = await api.patch(`/admin/events/${eventId}/status`, { status })
        this.message = 'Status eveniment actualizat.'
        return data
      } catch (error) {
        this.error = getApiError(error, 'Nu pot valida evenimentul')
        throw error
      }
    },
    async sendFeedback(eventId, payload) {
      this.error = ''
      try {
        const { data } = await api.post(`/events/${eventId}/feedback`, payload)
        this.message = 'Feedback trimis.'
        return data
      } catch (error) {
        this.error = getApiError(error, 'Nu pot trimite feedback-ul')
        throw error
      }
    },
    clearMessage() {
      this.message = ''
    },
  },
})
