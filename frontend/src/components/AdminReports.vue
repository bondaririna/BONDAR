<script setup>
import { computed } from 'vue'

const props = defineProps({
  events: {
    type: Array,
    default: () => [],
  },
})

const byMonth = computed(() => {
  const map = {}
  props.events.forEach((ev) => {
    const d = new Date(ev.start_at)
    if (Number.isNaN(d.getTime())) return
    const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`
    map[key] = (map[key] || 0) + 1
  })
  return Object.entries(map).sort((a, b) => (a[0] > b[0] ? 1 : -1))
})

const byOrganizer = computed(() => {
  const map = {}
  props.events.forEach((ev) => {
    const key = ev.organizer_name || 'Nespecificat'
    map[key] = (map[key] || 0) + 1
  })
  return Object.entries(map).sort((a, b) => b[1] - a[1])
})

const statusCounts = computed(() => {
  const res = { draft: 0, pending: 0, published: 0, rejected: 0 }
  props.events.forEach((ev) => {
    if (res[ev.status] !== undefined) res[ev.status] += 1
  })
  return res
})
</script>

<template>
  <section class="card">
    <h3>Rapoarte rapide (client-side)</h3>
    <div class="grid">
      <div class="stat">
        <p class="label">Published</p>
        <p class="value">{{ statusCounts.published }}</p>
      </div>
      <div class="stat">
        <p class="label">Pending</p>
        <p class="value">{{ statusCounts.pending }}</p>
      </div>
      <div class="stat">
        <p class="label">Draft</p>
        <p class="value">{{ statusCounts.draft }}</p>
      </div>
      <div class="stat">
        <p class="label">Rejected</p>
        <p class="value">{{ statusCounts.rejected }}</p>
      </div>
    </div>

    <div class="columns">
      <div class="card inner">
        <h4>Evenimente / lună</h4>
        <p v-if="!byMonth.length" class="muted">Nu există date.</p>
        <ul v-else>
          <li v-for="[month, count] in byMonth" :key="month">
            <strong>{{ month }}</strong>: {{ count }}
          </li>
        </ul>
      </div>

      <div class="card inner">
        <h4>Evenimente / organizator</h4>
        <p v-if="!byOrganizer.length" class="muted">Nu există date.</p>
        <ul v-else>
          <li v-for="[org, count] in byOrganizer" :key="org">
            <strong>{{ org }}</strong>: {{ count }}
          </li>
        </ul>
      </div>
    </div>

    <p class="muted">
      Participare medie și rapoarte PDF necesită date suplimentare (participanți/feedback) și/sau endpoint dedicat în backend.
    </p>
  </section>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 0.75rem;
}
.stat {
  padding: 0.7rem;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
}
.label {
  margin: 0;
  color: #555;
}
.value {
  margin: 0.15rem 0 0;
  font-size: 1.2rem;
  font-weight: 700;
}
.columns {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 0.75rem;
  margin-top: 0.75rem;
}
.inner {
  border: 1px solid #e5e5e5;
}
.muted {
  color: #555;
}
ul {
  padding-left: 1rem;
  margin: 0.5rem 0 0;
}
li {
  margin: 0.1rem 0;
}
</style>
