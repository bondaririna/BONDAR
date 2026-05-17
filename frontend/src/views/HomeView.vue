<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const role = computed(() => auth.user?.role || 'guest')
</script>

<template>
  <div class="home">
    <section class="hero card">
      <div>
        <p class="pill">Platforma USV Events</p>
        <h2>Descoperă, organizează și validează evenimentele campusului</h2>
        <p class="lead">
          O experiență unificată pentru studenți, organizatori și administratori: listă + calendar, feedback, validare și
          rapoarte.
        </p>
        <div class="actions">
          <RouterLink class="btn" to="/events">Vezi evenimente</RouterLink>
          <RouterLink v-if="!auth.isAuthenticated" class="btn secondary" to="/login">Autentificare</RouterLink>
        </div>
        <p v-if="auth.user" class="muted">Ești autentificat ca {{ auth.user.email }} ({{ role }})</p>
      </div>
      <div class="hero-panel">
        <ul>
          <li>Autentificare Google pentru studenți @student.usv.ro</li>
          <li>Autentificare user/parolă pentru organizatori și admini</li>
          <li>Calendar interactiv + filtri avansați</li>
          <li>QR, înscriere, feedback, status publicare</li>
          <li>Rapoarte rapide pentru admin</li>
        </ul>
      </div>
    </section>

    <section class="grid-3">
      <article class="card">
        <p class="pill">Student</p>
        <h3>Descoperă evenimente</h3>
        <p>Afișare listă + calendar, filtri detaliați, QR, înscriere, export Google/ICS și feedback după eveniment.</p>
        <div class="mini-actions">
          <RouterLink class="btn secondary" to="/events">Evenimente</RouterLink>
        </div>
      </article>

      <article class="card">
        <p class="pill">Organizator</p>
        <h3>Gestionează evenimentele tale</h3>
        <p>Creare, editare, ștergere, status draft/pending, sponsori, QR, link înscriere, panouri participanți/materiale (ready for API).</p>
        <div class="mini-actions">
          <RouterLink class="btn secondary" v-if="auth.isOrganizer || auth.isAdmin" to="/organizer/events">
            Dashboard
          </RouterLink>
          <RouterLink class="btn" v-if="auth.isOrganizer || auth.isAdmin" to="/organizer/new-event">
            Nou eveniment
          </RouterLink>
          <RouterLink class="btn secondary" v-else to="/login">Autentificare organizator</RouterLink>
        </div>
      </article>

      <article class="card">
        <p class="pill">Administrator</p>
        <h3>Validează și raportează</h3>
        <p>Validare publish/reject, creare organizatori, rapoarte rapide (per lună, per organizator, statusuri).</p>
        <div class="mini-actions">
          <RouterLink class="btn secondary" v-if="auth.isAdmin" to="/admin/validate">Panou admin</RouterLink>
          <RouterLink class="btn secondary" v-else to="/login">Autentificare admin</RouterLink>
        </div>
      </article>
    </section>
  </div>
</template>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.hero {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.2rem;
  background: radial-gradient(circle at 20% 20%, #e8f1ff 0, #fff 35%), #fff;
}

.hero h2 {
  margin: 0.3rem 0 0.4rem;
  line-height: 1.2;
}

.lead {
  margin: 0.2rem 0 0.6rem;
  color: #3d4a5f;
}

.actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin: 0.6rem 0;
}

.muted {
  color: #63738a;
}

.hero-panel {
  padding: 0.8rem;
  border: 1px dashed #d7dbe6;
  border-radius: 12px;
  background: #f9fbff;
}

.hero-panel ul {
  margin: 0.4rem 0 0;
  padding-left: 1.2rem;
  color: #3d4a5f;
  display: grid;
  gap: 0.25rem;
}

.mini-actions {
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
  margin-top: 0.6rem;
}
</style>
