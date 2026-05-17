<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
  submitLabel: {
    type: String,
    default: 'Salvează',
  },
  loading: {
    type: Boolean,
    default: false,
  },
  showStatus: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:modelValue', 'submit'])

const local = reactive({ ...props.modelValue })

watch(
  () => props.modelValue,
  (val) => {
    Object.assign(local, val)
  },
  { deep: true },
)

function updateField(key, value) {
  local[key] = value
  emit('update:modelValue', { ...local })
}

function toIso(value) {
  const d = new Date(value)
  return Number.isNaN(d.getTime()) ? '' : d.toISOString()
}

function handleSubmit() {
  const payload = {
    ...local,
    start_at: toIso(local.start_at),
    end_at: toIso(local.end_at),
    sponsors_json: local.sponsors_json || null,
    registration_link: local.registration_link || null,
    qr_payload: local.qr_payload || null,
  }
  emit('submit', payload)
}
</script>

<template>
  <form class="event-form" @submit.prevent="handleSubmit">
    <div class="form-row">
      <label for="title">Titlu</label>
      <input id="title" :value="local.title" required @input="updateField('title', $event.target.value)" />
    </div>

    <div class="form-row">
      <label for="description">Descriere</label>
      <textarea id="description" :value="local.description" rows="3" @input="updateField('description', $event.target.value)" />
    </div>

    <div class="grid-2">
      <div class="form-row">
        <label for="start">Start</label>
        <input
          id="start"
          type="datetime-local"
          :value="local.start_at"
          required
          @input="updateField('start_at', $event.target.value)"
        />
      </div>
      <div class="form-row">
        <label for="end">End</label>
        <input id="end" type="datetime-local" :value="local.end_at" required @input="updateField('end_at', $event.target.value)" />
      </div>
    </div>

    <div class="grid-2">
      <div class="form-row">
        <label for="category">Categorie</label>
        <select id="category" :value="local.category" @change="updateField('category', $event.target.value)">
          <option value="academic">Academic</option>
          <option value="sport">Sport</option>
          <option value="career">Carieră</option>
          <option value="volunteering">Voluntariat</option>
          <option value="cultural">Cultural</option>
          <option value="other">Altele</option>
        </select>
      </div>
      <div class="form-row">
        <label for="mode">Participare</label>
        <select id="mode" :value="local.participation_mode" @change="updateField('participation_mode', $event.target.value)">
          <option value="physical">Fizic</option>
          <option value="online">Online</option>
          <option value="hybrid">Hibrid</option>
        </select>
      </div>
    </div>

    <div class="grid-2">
      <div class="form-row">
        <label for="location">Locație</label>
        <input id="location" :value="local.location" @input="updateField('location', $event.target.value)" />
      </div>
      <div class="form-row">
        <label for="faculty">Facultate / Departament</label>
        <input id="faculty" :value="local.faculty_or_department" @input="updateField('faculty_or_department', $event.target.value)" />
      </div>
    </div>

    <div class="form-row">
      <label for="organizer">Nume organizator</label>
      <input id="organizer" :value="local.organizer_name" @input="updateField('organizer_name', $event.target.value)" />
    </div>

    <div class="form-row">
      <label for="registration">Link înscriere</label>
      <input id="registration" :value="local.registration_link" @input="updateField('registration_link', $event.target.value)" />
    </div>

    <div class="form-row">
      <label for="qr">QR payload</label>
      <input id="qr" :value="local.qr_payload" @input="updateField('qr_payload', $event.target.value)" />
    </div>

    <div class="form-row">
      <label for="sponsors">Sponsors JSON</label>
      <textarea id="sponsors" :value="local.sponsors_json" rows="2" @input="updateField('sponsors_json', $event.target.value)" />
    </div>

    <div class="grid-2">
      <label><input type="checkbox" :checked="local.requires_registration" @change="updateField('requires_registration', $event.target.checked)" /> Necesită înscriere</label>
      <label><input type="checkbox" :checked="local.free_entry" @change="updateField('free_entry', $event.target.checked)" /> Intrare gratuită</label>
    </div>

    <div v-if="showStatus" class="form-row">
      <label for="status">Status</label>
      <select id="status" :value="local.status || 'draft'" @change="updateField('status', $event.target.value)">
        <option value="draft">Draft</option>
        <option value="pending">Pending</option>
        <option value="published">Published</option>
        <option value="rejected">Rejected</option>
      </select>
      <p class="hint">Organizatorii pot seta draft/pending; publicarea finală rămâne la admin.</p>
    </div>

    <div class="actions">
      <button class="btn" type="submit" :disabled="loading">{{ loading ? 'Se salvează...' : submitLabel }}</button>
    </div>
  </form>
</template>

<style scoped>
.event-form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.hint {
  margin: 0.25rem 0 0;
  color: #555;
  font-size: 0.9rem;
}
</style>
