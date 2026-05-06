<script setup>
import { onMounted, reactive } from 'vue'
import { RouterLink } from 'vue-router'

import { useAuthStore } from '@/stores/auth'
import { useEventsStore } from '@/stores/events'

const auth = useAuthStore()
const events = useEventsStore()

const filters = reactive({
  q: '',
  category: '',
  participation_mode: '',
})

const feedbackDraft = reactive({})

async function loadEvents() {
  const params = {}
  if (filters.q) params.q = filters.q
  if (filters.category) params.category = filters.category
  if (filters.participation_mode) params.participation_mode = filters.participation_mode
  await events.fetchEvents(params)
}

function initFeedback(id) {
  if (!feedbackDraft[id]) {
    feedbackDraft[id] = { rating: 5, comment: '' }
  }
}

async function submitFeedback(eventId) {
  initFeedback(eventId)
  await events.sendFeedback(eventId, feedbackDraft[eventId])
}

onMounted(loadEvents)
</script>

<template>
  <section class="card">
    <h2>Evenimente</h2>
    <div class="grid-2">
      <div class="form-row">
        <label for="q">Cautare</label>
        <input id="q" v-model="filters.q" placeholder="Titlu sau descriere" />
      </div>
      <div class="form-row">
        <label for="category">Categorie</label>
        <select id="category" v-model="filters.category">
          <option value="">Toate</option>
          <option value="academic">Academic</option>
          <option value="sport">Sport</option>
          <option value="career">Career</option>
          <option value="volunteering">Volunteering</option>
          <option value="cultural">Cultural</option>
          <option value="other">Other</option>
        </select>
      </div>
    </div>
    <button class="btn" type="button" @click="loadEvents">Aplica filtre</button>
    <p v-if="events.error" class="error">{{ events.error }}</p>
    <p v-if="events.message" class="success">{{ events.message }}</p>
  </section>

  <section v-if="events.loading" class="card">
    <p>Se incarca evenimentele...</p>
  </section>

  <section v-for="ev in events.items" :key="ev.id" class="card">
    <h3>{{ ev.title }}</h3>
    <p>{{ ev.description || 'Fara descriere' }}</p>
    <p><strong>Status:</strong> {{ ev.status }}</p>
    <p><strong>Perioada:</strong> {{ new Date(ev.start_at).toLocaleString() }} - {{ new Date(ev.end_at).toLocaleString() }}</p>
    <p><strong>Locatie:</strong> {{ ev.location || '-' }}</p>
    <p><strong>Organizator:</strong> {{ ev.organizer_name || '-' }}</p>

    <p v-if="!auth.isAuthenticated">
      Functionalitatile critice (ex: feedback) necesita autentificare.
      <RouterLink to="/login">Autentifica-te</RouterLink>.
    </p>
    <p v-else-if="!auth.isStudent">
      Feedback-ul este disponibil doar pentru conturile student.
    </p>

    <div v-if="auth.isStudent">
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
      <button class="btn secondary" type="button" @click="submitFeedback(ev.id)">Trimite</button>
    </div>
  </section>
</template>
