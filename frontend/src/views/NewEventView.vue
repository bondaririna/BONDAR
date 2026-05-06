<script setup>
import { reactive } from 'vue'

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

async function onSubmit() {
  const payload = {
    ...form,
    start_at: new Date(form.start_at).toISOString(),
    end_at: new Date(form.end_at).toISOString(),
    sponsors_json: form.sponsors_json || null,
    registration_link: form.registration_link || null,
    qr_payload: form.qr_payload || null,
  }
  await events.createEvent(payload)
}
</script>

<template>
  <section class="card">
    <h2>Creeaza Eveniment</h2>
    <form @submit.prevent="onSubmit">
      <div class="form-row">
        <label for="title">Titlu</label>
        <input id="title" v-model="form.title" required />
      </div>

      <div class="form-row">
        <label for="description">Descriere</label>
        <textarea id="description" v-model="form.description" rows="3" />
      </div>

      <div class="grid-2">
        <div class="form-row">
          <label for="start">Start</label>
          <input id="start" v-model="form.start_at" type="datetime-local" required />
        </div>
        <div class="form-row">
          <label for="end">End</label>
          <input id="end" v-model="form.end_at" type="datetime-local" required />
        </div>
      </div>

      <div class="grid-2">
        <div class="form-row">
          <label for="category">Categorie</label>
          <select id="category" v-model="form.category">
            <option value="academic">Academic</option>
            <option value="sport">Sport</option>
            <option value="career">Career</option>
            <option value="volunteering">Volunteering</option>
            <option value="cultural">Cultural</option>
            <option value="other">Other</option>
          </select>
        </div>
        <div class="form-row">
          <label for="mode">Participare</label>
          <select id="mode" v-model="form.participation_mode">
            <option value="physical">Physical</option>
            <option value="online">Online</option>
            <option value="hybrid">Hybrid</option>
          </select>
        </div>
      </div>

      <div class="grid-2">
        <div class="form-row">
          <label for="location">Locatie</label>
          <input id="location" v-model="form.location" />
        </div>
        <div class="form-row">
          <label for="faculty">Facultate / Departament</label>
          <input id="faculty" v-model="form.faculty_or_department" />
        </div>
      </div>

      <div class="form-row">
        <label for="organizer">Nume organizator</label>
        <input id="organizer" v-model="form.organizer_name" />
      </div>
      <div class="form-row">
        <label for="registration">Link inscriere</label>
        <input id="registration" v-model="form.registration_link" />
      </div>
      <div class="form-row">
        <label for="qr">QR payload</label>
        <input id="qr" v-model="form.qr_payload" />
      </div>
      <div class="form-row">
        <label for="sponsors">Sponsors JSON</label>
        <textarea id="sponsors" v-model="form.sponsors_json" rows="2" />
      </div>

      <div class="grid-2">
        <label><input v-model="form.requires_registration" type="checkbox" /> Necesita inscriere</label>
        <label><input v-model="form.free_entry" type="checkbox" /> Intrare gratuita</label>
      </div>

      <p v-if="events.error" class="error">{{ events.error }}</p>
      <p v-if="events.message" class="success">{{ events.message }}</p>
      <button class="btn" type="submit">Salveaza</button>
    </form>
  </section>
</template>
