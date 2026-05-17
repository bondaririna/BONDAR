<template>
  <div class="app-shell">
    <header class="topbar">
      <div class="brand">
        <div class="dot" />
        <div>
          <p class="subtitle">USV Campus</p>
          <h1>Event Hub</h1>
        </div>
      </div>

      <nav class="menu">
        <RouterLink to="/">Acasă</RouterLink>
        <RouterLink to="/events">Evenimente</RouterLink>
        <RouterLink v-if="auth.isOrganizer || auth.isAdmin" to="/organizer/events">
          Evenimentele mele
        </RouterLink>
        <RouterLink v-if="auth.isOrganizer || auth.isAdmin" to="/organizer/new-event">
          Creează eveniment
        </RouterLink>
        <RouterLink v-if="auth.isAdmin" to="/admin/validate">Admin</RouterLink>
      </nav>

      <div class="auth-box">
        <span v-if="auth.user" class="user-chip">
          {{ auth.user.full_name || auth.user.email }} <span class="pill">{{ auth.user.role }}</span>
        </span>
        <RouterLink v-if="!auth.isAuthenticated" class="btn secondary" to="/login">Autentificare</RouterLink>
        <button v-else type="button" class="btn" @click="logout">Logout</button>
      </div>
    </header>

    <div class="page">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'

import { useAuthStore } from './stores/auth'

const auth = useAuthStore()

onMounted(async () => {
  auth.initFromStorage()
  if (auth.token && !auth.user) {
    await auth.fetchMe()
  }
})

function logout() {
  auth.logout()
}
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 10;
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 1rem;
  align-items: center;
  border-bottom: 1px solid #e6eaf2;
  padding: 0.85rem 1.4rem;
  background: rgba(255, 255, 255, 0.94);
  backdrop-filter: blur(10px);
}

.brand {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.dot {
  width: 38px;
  height: 38px;
  border-radius: 12px;
  background: linear-gradient(135deg, #1f64c6, #2d8bff);
  box-shadow: 0 6px 18px rgba(45, 139, 255, 0.25);
}

.subtitle {
  margin: 0;
  color: #4b5563;
  font-size: 0.9rem;
}

.menu {
  display: flex;
  gap: 0.8rem;
  align-items: center;
  justify-content: center;
}

.menu {
  display: flex;
  gap: 0.8rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.2rem;
}

.auth-box {
  display: flex;
  gap: 0.6rem;
  align-items: center;
}

.user-chip {
  display: inline-flex;
  gap: 0.35rem;
  align-items: center;
  padding: 0.35rem 0.55rem;
  border-radius: 10px;
  background: #eef2f7;
  font-weight: 600;
  color: #1f2c3d;
}

.page {
  padding: 1.2rem;
}
</style>
