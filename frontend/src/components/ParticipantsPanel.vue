<script setup>
const props = defineProps({
  participants: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['export', 'checkin'])

function exportList() {
  emit('export')
}

function checkIn(id) {
  emit('checkin', id)
}
</script>

<template>
  <section class="card section">
    <div class="header">
      <div>
        <h4>Participanți</h4>
        <p class="muted">Listă/Export/Check-in (necesită endpoint backend)</p>
      </div>
      <div class="actions">
        <button class="btn" type="button" disabled @click="exportList">Export CSV</button>
      </div>
    </div>

    <p v-if="!participants.length" class="muted">Nu sunt participanți disponibili (API indisponibil încă).</p>
    <table v-else class="table">
      <thead>
        <tr>
          <th>Nume</th>
          <th>Email</th>
          <th>Status</th>
          <th />
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in participants" :key="p.id">
          <td>{{ p.name }}</td>
          <td>{{ p.email }}</td>
          <td>{{ p.status || 'inscris' }}</td>
          <td><button class="btn secondary" type="button" disabled @click="checkIn(p.id)">Check-in</button></td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<style scoped>
.section {
  margin-top: 0.5rem;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
}
.actions {
  display: flex;
  gap: 0.5rem;
}
.muted {
  color: #555;
  margin: 0;
}
.table {
  width: 100%;
  border-collapse: collapse;
}
.table th,
.table td {
  text-align: left;
  padding: 0.4rem 0.35rem;
  border-bottom: 1px solid #e5e5e5;
}
</style>
