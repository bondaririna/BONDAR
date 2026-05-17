<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { RouterLink } from 'vue-router'

import EventCard from '@/components/EventCard.vue'
import EventForm from '@/components/EventForm.vue'
import MaterialsPanel from '@/components/MaterialsPanel.vue'
import OrganizerStats from '@/components/OrganizerStats.vue'
import ParticipantsPanel from '@/components/ParticipantsPanel.vue'
import { useAuthStore } from '@/stores/auth'
import { useEventsStore } from '@/stores/events'

const auth = useAuthStore()
const events = useEventsStore()

const editingId = ref(null)
const editForm = reactive(getEmptyForm())

const myEvents = computed(() => {
  if (auth.isAdmin) return events.items
  if (!auth.user) return []
  return events.items.filter((ev) => ev.organizer_user_id === auth.user.id)
})

function getEmptyForm() {
  return {
    title: '',
    description: '',
    start_at: '',
    end_at: '',
    location: '',
    faculty_or_department: '',
    category: 'academic',
    participation_mode: 'physical',
    organizer_name: auth.user?.full_name || '',
    registration_link: '',
    qr_payload: '',
    sponsors_json: '',
    requires_registration: false,
    free_entry: true,
    status: 'draft',
  }
}

function toLocalInput(dateStr) {
  const d = new Date(dateStr)
  if (Number.isNaN(d.getTime())) return ''
  const iso = d.toISOString()
  return iso.slice(0, 16)
}

async function load() {
  await events.fetchEvents()
}

function startEdit(ev) {
  editingId.value = ev.id
  Object.assign(editForm, getEmptyForm(), {
    ...ev,
    start_at: toLocalInput(ev.start_at),
    end_at: toLocalInput(ev.end_at),
  })
}

function cancelEdit() {
  editingId.value = null
  Object.assign(editForm, getEmptyForm())
}

async function saveEdit(payload) {
  if (!editingId.value) return
  await events.updateEvent(editingId.value, payload)
  await load()
  cancelEdit()
}

async function remove(ev) {
  if (!confirm('Ștergi acest eveniment?')) return
  await events.deleteEvent(ev.id)
  await load()
}

onMounted(load)
</script>

<template>
  <section class="card">
    <div class="header">
      <div>
        <h2>Evenimentele mele</h2>
        <p class="muted">Creare, editare și ștergere</p>
      </div>
      <RouterLink class="btn" to="/organizer/new-event">Creează eveniment</RouterLink>
    </div>
    <p v-if="events.error" class="error">{{ events.error }}</p>
    <p v-if="events.message" class="success">{{ events.message }}</p>
  </section>

  <section v-if="events.loading" class="card">
    <p>Se încarcă evenimentele...</p>
  </section>

  <section v-else-if="myEvents.length === 0" class="card">
    <p>Nu ai încă evenimente create.</p>
  </section>

  <section v-else class="list">
    <EventCard v-for="ev in myEvents" :key="ev.id" :event="ev" @download-ics="() => {}">
      <div class="actions">
        <button class="btn secondary" type="button" @click="startEdit(ev)">Editează</button>
        <button class="btn" type="button" @click="remove(ev)">Șterge</button>
      </div>
      <ParticipantsPanel />
      <MaterialsPanel />
    </EventCard>
  </section>

  <section v-if="editingId" class="card">
    <div class="header">
      <h3>Editează eveniment</h3>
      <button class="btn secondary" type="button" @click="cancelEdit">Renunță</button>
    </div>
    <EventForm
      v-model:modelValue="editForm"
      submit-label="Actualizează"
      :loading="events.loading"
      :show-status="true"
      @submit="saveEdit"
    />
  </section>

  <OrganizerStats :events="myEvents" />
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.muted {
  color: #555;
  margin: 0;
}

.list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: 0.5rem;
}
</style>
