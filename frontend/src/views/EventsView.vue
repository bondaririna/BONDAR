<script setup>
import { onMounted, reactive, ref, computed } from 'vue'
import VueCal from 'vue-cal'
import 'vue-cal/dist/vuecal.css'

import { useAuthStore } from '@/stores/auth'
import { useEventsStore } from '@/stores/events'
import EventCard from '@/components/EventCard.vue'
import EventFilters from '@/components/EventFilters.vue'

const auth = useAuthStore()
const events = useEventsStore()

const viewMode = ref('list')
const feedbackDraft = reactive({})
const filters = reactive({
  q: '',
  faculty_or_department: '',
  date_from: '',
  date_to: '',
  category: '',
  location: '',
  organizer_name: '',
  participation_mode: '',
  free_entry: '',
  requires_registration: '',
  has_qr: '',
})

const calendarEvents = computed(() =>
  events.items.map((ev) => ({
    title: ev.title,
    start: ev.start_at,
    end: ev.end_at,
    content: ev.description,
    class: `status-${ev.status}`,
  })),
)

function cleanParams(raw) {
  const params = {}
  const map = { ...raw }
  if (map.q) params.q = map.q
  if (map.faculty_or_department) params.faculty_or_department = map.faculty_or_department
  if (map.date_from) params.date_from = map.date_from
  if (map.date_to) params.date_to = map.date_to
  if (map.category) params.category = map.category
  if (map.location) params.location = map.location
  if (map.organizer_name) params.organizer_name = map.organizer_name
  if (map.participation_mode) params.participation_mode = map.participation_mode
  if (map.free_entry === true || map.free_entry === false) params.free_entry = map.free_entry
  if (map.requires_registration === true || map.requires_registration === false)
    params.requires_registration = map.requires_registration
  if (map.has_qr === true || map.has_qr === false) params.has_qr = map.has_qr
  return params
}

async function loadEvents(payload = filters) {
  const params = cleanParams(payload)
  await events.fetchEvents(params)
}

function onFiltersApply(payload) {
  Object.assign(filters, payload)
  loadEvents(payload)
}

function initFeedback(id) {
  if (!feedbackDraft[id]) {
    feedbackDraft[id] = { rating: 5, comment: '' }
  }
}

function eventEnded(ev) {
  const now = Date.now()
  return new Date(ev.end_at).getTime() <= now
}

async function submitFeedback(eventId) {
  initFeedback(eventId)
  await events.sendFeedback(eventId, feedbackDraft[eventId])
}

function formatIcsDate(dateStr) {
  const d = new Date(dateStr)
  return d.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z'
}

function downloadIcs(ev) {
  const lines = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//Campus Events//EN',
    'BEGIN:VEVENT',
    `UID:${ev.id}@campus-events`,
    `DTSTAMP:${formatIcsDate(new Date().toISOString())}`,
    `DTSTART:${formatIcsDate(ev.start_at)}`,
    `DTEND:${formatIcsDate(ev.end_at)}`,
    `SUMMARY:${ev.title}`,
    `DESCRIPTION:${(ev.description || '').replace(/\n/g, '\\n')}`,
    `LOCATION:${ev.location || ''}`,
    ev.registration_link ? `URL:${ev.registration_link}` : null,
    'END:VEVENT',
    'END:VCALENDAR',
  ].filter(Boolean)

  const blob = new Blob([lines.join('\r\n')], { type: 'text/calendar' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${ev.title || 'eveniment'}.ics`
  a.click()
  URL.revokeObjectURL(url)
}

onMounted(() => loadEvents(filters))
</script>

<template>
  <section class="card header">
    <div>
      <h2>Evenimente</h2>
      <p class="muted">Listă și calendar cu filtre detaliate</p>
    </div>
    <div class="view-toggle">
      <button class="btn" :class="{ secondary: viewMode !== 'list' }" type="button" @click="viewMode = 'list'">
        Listă
      </button>
      <button class="btn" :class="{ secondary: viewMode !== 'calendar' }" type="button" @click="viewMode = 'calendar'">
        Calendar
      </button>
    </div>
  </section>

  <EventFilters v-model:modelValue="filters" @apply="onFiltersApply" />

  <p v-if="events.error" class="error">{{ events.error }}</p>
  <p v-if="events.message" class="success">{{ events.message }}</p>

  <section v-if="events.loading" class="card">
    <p>Se încarcă evenimentele...</p>
  </section>

  <template v-else>
    <section v-if="viewMode === 'calendar'" class="card">
      <VueCal :events="calendarEvents" hide-view-selector default-view="month" style="min-height: 640px" />
    </section>

    <section v-if="events.items.length === 0" class="card">
      <p>Nu există evenimente pentru filtrele curente.</p>
    </section>

    <EventCard v-for="ev in events.items" v-else :key="ev.id" :event="ev" @download-ics="downloadIcs">
      <div class="feedback-box" v-if="auth.isStudent">
        <h4>Trimite feedback</h4>
        <div class="grid-2">
          <div class="form-row">
            <label>Rating</label>
            <input
              type="number"
              min="1"
              max="5"
              step="0.5"
              :value="feedbackDraft[ev.id]?.rating ?? 5"
              @input="initFeedback(ev.id); feedbackDraft[ev.id].rating = Number($event.target.value)"
            />
          </div>
          <div class="form-row">
            <label>Comentariu</label>
            <input
              type="text"
              :value="feedbackDraft[ev.id]?.comment ?? ''"
              @input="initFeedback(ev.id); feedbackDraft[ev.id].comment = $event.target.value"
            />
          </div>
        </div>
        <p class="muted" v-if="!eventEnded(ev)">Feedback disponibil după încheierea evenimentului.</p>
        <button class="btn secondary" type="button" :disabled="!eventEnded(ev)" @click="submitFeedback(ev.id)">
          Trimite
        </button>
      </div>

      <div v-else-if="!auth.isAuthenticated" class="muted">
        Funcționalitățile critice (feedback, înscriere) necesită autentificare.
      </div>
    </EventCard>
  </template>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: center;
}

.view-toggle {
  display: flex;
  gap: 0.5rem;
}

.feedback-box {
  margin-top: 0.75rem;
  padding-top: 0.5rem;
  border-top: 1px solid #e5e5e5;
}

.muted {
  color: #555;
  margin: 0;
}

:deep(.vuecal__event.status-published) {
  background: #e6f4ea;
  border-color: #0f9d58;
  color: #0f9d58;
}

:deep(.vuecal__event.status-pending) {
  background: #fff4e5;
  border-color: #c87200;
  color: #c87200;
}

:deep(.vuecal__event.status-rejected),
:deep(.vuecal__event.status-draft) {
  background: #f7d7da;
  border-color: #a50e0e;
  color: #a50e0e;
}
</style>
