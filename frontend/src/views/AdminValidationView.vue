<script setup>
import { computed, onMounted, reactive, ref } from 'vue'

import EventCard from '@/components/EventCard.vue'
import AdminReports from '@/components/AdminReports.vue'
import api, { getApiError } from '@/services/api'
import { useEventsStore } from '@/stores/events'

const events = useEventsStore()

const statusFilter = ref('pending')
const organizerForm = reactive({
  email: '',
  full_name: '',
  password: '',
})
const creating = ref(false)
const organizerMessage = ref('')
const organizerError = ref('')

const filteredEvents = computed(() => {
  if (!statusFilter.value) return events.items
  return events.items.filter((ev) => ev.status === statusFilter.value)
})

async function loadAll() {
  await events.fetchEvents()
}

async function setStatus(id, status) {
  await events.validateEvent(id, status)
  await loadAll()
}

async function createOrganizer() {
  organizerError.value = ''
  organizerMessage.value = ''
  creating.value = true
  try {
    await api.post('/admin/organizers', { ...organizerForm, role: 'organizer' })
    organizerMessage.value = 'Organizator creat.'
    organizerForm.email = ''
    organizerForm.full_name = ''
    organizerForm.password = ''
  } catch (error) {
    organizerError.value = getApiError(error, 'Nu pot crea organizatorul')
  } finally {
    creating.value = false
  }
}

onMounted(loadAll)
</script>

<template>
  <section class="card">
    <div class="header">
      <div>
        <h2>Validare Evenimente (Admin)</h2>
        <p class="muted">Publică sau respinge evenimentele propuse</p>
      </div>
      <div class="controls">
        <label>
          Filtru status
          <select v-model="statusFilter">
            <option value="">Toate</option>
            <option value="pending">Pending</option>
            <option value="draft">Draft</option>
            <option value="published">Published</option>
            <option value="rejected">Rejected</option>
          </select>
        </label>
        <button class="btn" type="button" @click="loadAll">Reîncarcă</button>
      </div>
    </div>
    <p v-if="events.error" class="error">{{ events.error }}</p>
    <p v-if="events.message" class="success">{{ events.message }}</p>
  </section>

  <section v-if="events.loading" class="card">
    <p>Se încarcă evenimentele...</p>
  </section>

  <section v-else-if="filteredEvents.length === 0" class="card">
    <p>Nu există evenimente pentru filtrul selectat.</p>
  </section>

  <section v-else class="list">
    <EventCard v-for="ev in filteredEvents" :key="ev.id" :event="ev" @download-ics="() => {}">
      <div class="actions">
        <button class="btn" type="button" @click="setStatus(ev.id, 'published')">Publish</button>
        <button class="btn secondary" type="button" @click="setStatus(ev.id, 'rejected')">Reject</button>
      </div>
    </EventCard>
  </section>

  <section class="card">
    <h3>Creează organizator</h3>
    <form class="grid-3" @submit.prevent="createOrganizer">
      <div class="form-row">
        <label for="email">Email</label>
        <input id="email" v-model="organizerForm.email" type="email" required />
      </div>
      <div class="form-row">
        <label for="full_name">Nume</label>
        <input id="full_name" v-model="organizerForm.full_name" />
      </div>
      <div class="form-row">
        <label for="password">Parolă</label>
        <input id="password" v-model="organizerForm.password" type="password" required minlength="8" />
      </div>
      <button class="btn" type="submit" :disabled="creating">{{ creating ? 'Se creează...' : 'Creează' }}</button>
    </form>
    <p v-if="organizerError" class="error">{{ organizerError }}</p>
    <p v-if="organizerMessage" class="success">{{ organizerMessage }}</p>
  </section>

  <AdminReports :events="events.items" />
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: center;
}

.controls {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.muted {
  color: #555;
  margin: 0;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.75rem;
  align-items: end;
}
</style>
