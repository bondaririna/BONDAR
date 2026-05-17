<script setup>
import { reactive } from 'vue'

import EventForm from '@/components/EventForm.vue'
import { useEventsStore } from '@/stores/events'

const events = useEventsStore()

const form = reactive({
  title: '',
  description: '',
  start_at: '',
  end_at: '',
  location: '',
  faculty_or_department: '',
  category: 'academic',
  participation_mode: 'physical',
  organizer_name: '',
  registration_link: '',
  qr_payload: '',
  sponsors_json: '',
  requires_registration: false,
  free_entry: true,
})

async function handleSubmit(payload) {
  await events.createEvent(payload)
}
</script>

<template>
  <section class="card">
    <h2>Creează Eveniment</h2>
    <EventForm
      v-model:modelValue="form"
      submit-label="Salvează"
      :loading="events.loading"
      :show-status="true"
      @submit="handleSubmit"
    />
    <p v-if="events.error" class="error">{{ events.error }}</p>
    <p v-if="events.message" class="success">{{ events.message }}</p>
  </section>
</template>
