<script setup>
const emit = defineEmits(['upload'])

function onUpload(event) {
  const files = event.target.files || []
  emit('upload', files)
}
</script>

<template>
  <section class="card section">
    <div class="header">
      <div>
        <h4>Materiale eveniment</h4>
        <p class="muted">Prezentări/poze/PDF – necesită endpoint backend</p>
      </div>
      <div class="actions">
        <input type="file" multiple disabled @change="onUpload" />
        <button class="btn" type="button" disabled>Încarcă</button>
      </div>
    </div>
    <p class="muted">Funcționalitatea va fi activă după expunerea rutei de upload în backend.</p>
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
  flex-wrap: wrap;
}
.actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}
.muted {
  color: #555;
  margin: 0;
}
</style>
