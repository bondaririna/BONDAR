<script setup>
import { computed } from 'vue'

const props = defineProps({
  events: {
    type: Array,
    default: () => [],
  },
})

const totals = computed(() => {
  const byStatus = { draft: 0, pending: 0, published: 0, rejected: 0 }
  props.events.forEach((ev) => {
    if (byStatus[ev.status] !== undefined) byStatus[ev.status] += 1
  })
  return {
    count: props.events.length,
    ...byStatus,
  }
})
</script>

<template>
  <section class="card stats">
    <h4>Statistici rapide</h4>
    <div class="grid">
      <div class="stat">
        <p class="label">Total evenimente</p>
        <p class="value">{{ totals.count }}</p>
      </div>
      <div class="stat">
        <p class="label">Published</p>
        <p class="value">{{ totals.published }}</p>
      </div>
      <div class="stat">
        <p class="label">Pending</p>
        <p class="value">{{ totals.pending }}</p>
      </div>
      <div class="stat">
        <p class="label">Draft</p>
        <p class="value">{{ totals.draft }}</p>
      </div>
      <div class="stat">
        <p class="label">Rejected</p>
        <p class="value">{{ totals.rejected }}</p>
      </div>
    </div>
    <p class="muted">Feedback mediu/număr participanți necesită date din backend (feedbacks, participanți).</p>
  </section>
</template>

<style scoped>
.stats {
  margin-top: 0.5rem;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 0.75rem;
}
.stat {
  padding: 0.75rem;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
}
.label {
  margin: 0;
  color: #555;
}
.value {
  margin: 0.15rem 0 0;
  font-size: 1.3rem;
  font-weight: 700;
}
.muted {
  color: #555;
  margin-top: 0.5rem;
}
</style>
