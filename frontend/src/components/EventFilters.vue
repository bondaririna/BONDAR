<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['update:modelValue', 'apply'])

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

function toIsoOrNull(value) {
  if (!value) return null
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? null : date.toISOString()
}

function applyFilters() {
  const payload = {
    ...local,
    date_from: toIsoOrNull(local.date_from),
    date_to: toIsoOrNull(local.date_to),
  }

  const booleanKeys = ['free_entry', 'requires_registration', 'has_qr']
  booleanKeys.forEach((key) => {
    if (payload[key] === '') payload[key] = null
    else if (payload[key] === 'true') payload[key] = true
    else if (payload[key] === 'false') payload[key] = false
  })

  emit('apply', payload)
}

function resetFilters() {
  const cleared = {
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
  }
  emit('update:modelValue', cleared)
  Object.assign(local, cleared)
  applyFilters()
}
</script>

<template>
  <div class="filters card">
    <div class="filters-grid">
      <div class="form-row">
        <label for="q">Căutare</label>
        <input id="q" :value="local.q" placeholder="Titlu sau descriere" @input="updateField('q', $event.target.value)" />
      </div>

      <div class="form-row">
        <label for="faculty">Facultate/Departament</label>
        <input
          id="faculty"
          :value="local.faculty_or_department"
          placeholder="Ex: FIESC"
          @input="updateField('faculty_or_department', $event.target.value)"
        />
      </div>

      <div class="form-row">
        <label for="location">Locație</label>
        <input id="location" :value="local.location" @input="updateField('location', $event.target.value)" />
      </div>

      <div class="form-row">
        <label for="organizer">Organizator</label>
        <input
          id="organizer"
          :value="local.organizer_name"
          placeholder="Nume organizator"
          @input="updateField('organizer_name', $event.target.value)"
        />
      </div>

      <div class="form-row">
        <label for="category">Categorie</label>
        <select id="category" :value="local.category" @change="updateField('category', $event.target.value)">
          <option value="">Toate</option>
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
        <select
          id="mode"
          :value="local.participation_mode"
          @change="updateField('participation_mode', $event.target.value)"
        >
          <option value="">Toate</option>
          <option value="physical">Fizic</option>
          <option value="online">Online</option>
          <option value="hybrid">Hibrid</option>
        </select>
      </div>

      <div class="form-row">
        <label for="date_from">Data de la</label>
        <input
          id="date_from"
          type="datetime-local"
          :value="local.date_from"
          @input="updateField('date_from', $event.target.value)"
        />
      </div>

      <div class="form-row">
        <label for="date_to">Data până la</label>
        <input
          id="date_to"
          type="datetime-local"
          :value="local.date_to"
          @input="updateField('date_to', $event.target.value)"
        />
      </div>

      <div class="form-row">
        <label for="free_entry">Intrare</label>
        <select id="free_entry" :value="local.free_entry" @change="updateField('free_entry', $event.target.value)">
          <option value="">Toate</option>
          <option value="true">Gratuită</option>
          <option value="false">Cu taxă / condiții</option>
        </select>
      </div>

      <div class="form-row">
        <label for="requires_registration">Înscriere necesară</label>
        <select
          id="requires_registration"
          :value="local.requires_registration"
          @change="updateField('requires_registration', $event.target.value)"
        >
          <option value="">Toate</option>
          <option value="true">Da</option>
          <option value="false">Nu</option>
        </select>
      </div>

      <div class="form-row">
        <label for="has_qr">Cod QR</label>
        <select id="has_qr" :value="local.has_qr" @change="updateField('has_qr', $event.target.value)">
          <option value="">Toate</option>
          <option value="true">Are QR</option>
          <option value="false">Fără QR</option>
        </select>
      </div>
    </div>

    <div class="actions">
      <button class="btn" type="button" @click="applyFilters">Aplică filtre</button>
      <button class="btn secondary" type="button" @click="resetFilters">Reset</button>
    </div>
  </div>
</template>

<style scoped>
.filters {
  margin-bottom: 1rem;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 0.75rem 1rem;
}

.actions {
  margin-top: 0.75rem;
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}
</style>
