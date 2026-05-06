<script setup>
import { onMounted } from 'vue'

import { useEventsStore } from '@/stores/events'

const events = useEventsStore()

async function loadAll() {
  await events.fetchEvents()
}

async function setStatus(id, status) {
  await events.validateEvent(id, status)
  await loadAll()
}

onMounted(loadAll)
</script>

<template>
  <section class="card">
    <h2>Validare Evenimente (Admin)</h2>
    <button class="btn" type="button" @click="loadAll">Reincarca</button>
    <p v-if="events.error" class="error">{{ events.error }}</p>
    <p v-if="events.message" class="success">{{ events.message }}</p>
  </section>

  <section v-for="ev in events.items" :key="ev.id" class="card">
    <h3>{{ ev.title }}</h3>
    <p><strong>Status curent:</strong> {{ ev.status }}</p>
    <p>{{ ev.description || 'Fara descriere' }}</p>
    <div>
      <button class="btn" type="button" @click="setStatus(ev.id, 'published')">Publish</button>
      <button class="btn secondary" type="button" @click="setStatus(ev.id, 'rejected')">Reject</button>
    </div>
  </section>
</template>
