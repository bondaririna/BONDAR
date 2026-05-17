<script setup>
import { computed } from 'vue'
import QrcodeVue from 'qrcode.vue'

const props = defineProps({
  event: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['download-ics'])

const googleCalendarLink = computed(() => {
  if (!props.event?.start_at || !props.event?.end_at) return '#'
  const start = toCalendarDate(props.event.start_at)
  const end = toCalendarDate(props.event.end_at)
  const base = 'https://www.google.com/calendar/render?action=TEMPLATE'
  const params = new URLSearchParams({
    text: props.event.title || 'Eveniment',
    dates: `${start}/${end}`,
    details: props.event.description || '',
    location: props.event.location || '',
  })
  return `${base}&${params.toString()}`
})

function toCalendarDate(dateStr) {
  const d = new Date(dateStr)
  if (Number.isNaN(d.getTime())) return ''
  return d.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z'
}

function downloadIcs() {
  emit('download-ics', props.event)
}
</script>

<template>
  <article class="card event-card">
    <header class="event-head">
      <div>
        <h3>{{ event.title }}</h3>
        <p class="muted">{{ event.category }} · {{ event.participation_mode }}</p>
      </div>
      <span class="badge" :class="`status-${event.status}`">{{ event.status }}</span>
    </header>

    <p class="description">{{ event.description || 'Fără descriere' }}</p>

    <dl class="meta">
      <div>
        <dt>Perioadă</dt>
        <dd>{{ new Date(event.start_at).toLocaleString() }} - {{ new Date(event.end_at).toLocaleString() }}</dd>
      </div>
      <div>
        <dt>Locație</dt>
        <dd>{{ event.location || '-' }}</dd>
      </div>
      <div>
        <dt>Facultate/Dept.</dt>
        <dd>{{ event.faculty_or_department || '-' }}</dd>
      </div>
      <div>
        <dt>Organizator</dt>
        <dd>{{ event.organizer_name || '-' }}</dd>
      </div>
      <div>
        <dt>Participare</dt>
        <dd>{{ event.participation_mode }}</dd>
      </div>
      <div>
        <dt>Intrare</dt>
        <dd>{{ event.free_entry ? 'Gratuită' : 'Necesită taxă' }}</dd>
      </div>
      <div>
        <dt>Înscriere necesară</dt>
        <dd>{{ event.requires_registration ? 'Da' : 'Nu' }}</dd>
      </div>
    </dl>

    <div class="links" v-if="event.registration_link">
      <a :href="event.registration_link" target="_blank" rel="noreferrer">Link înscriere</a>
    </div>

    <div class="qr" v-if="event.qr_payload">
      <QrcodeVue :value="event.qr_payload" :size="120" level="M" />
      <p class="muted">Cod QR</p>
    </div>

    <div class="actions">
      <a class="btn secondary" :href="googleCalendarLink" target="_blank" rel="noreferrer">Adaugă în Google Calendar</a>
      <button class="btn" type="button" @click="downloadIcs">Descarcă .ics</button>
    </div>

    <slot />
  </article>
</template>

<style scoped>
.event-card {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.event-head {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: center;
}

.badge {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.85rem;
  text-transform: capitalize;
}

.status-published {
  background: #e6f4ea;
  color: #0f9d58;
}

.status-pending {
  background: #fff4e5;
  color: #c87200;
}

.status-draft,
.status-rejected {
  background: #f7d7da;
  color: #a50e0e;
}

.description {
  margin: 0;
}

.meta {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.35rem 0.75rem;
}

.meta dt {
  font-weight: 600;
  margin: 0;
}

.meta dd {
  margin: 0;
}

.links {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.qr {
  display: inline-flex;
  flex-direction: column;
  gap: 0.25rem;
  align-items: center;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.muted {
  color: #555;
  margin: 0;
}
</style>
