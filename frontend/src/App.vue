<template>
  <div class="app-shell">
    <header class="topbar">
      <h1>Campus Events</h1>
      <nav class="menu">
        <RouterLink to="/">Acasa</RouterLink>
        <RouterLink to="/events">Evenimente</RouterLink>
        <RouterLink v-if="auth.isOrganizer || auth.isAdmin" to="/organizer/new-event">
          Creeaza Eveniment
        </RouterLink>
        <RouterLink v-if="auth.isAdmin" to="/admin/validate">Validare Admin</RouterLink>
      </nav>
      <div class="auth-box">
        <span v-if="auth.user">{{ auth.user.email }} ({{ auth.user.role }})</span>
        <RouterLink v-if="!auth.isAuthenticated" to="/login">Login</RouterLink>
        <button v-else type="button" class="btn" @click="logout">Logout</button>
      </div>
    </header>

    <div class="container">
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
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #d8d8d8;
  padding: 0.8rem 1.2rem;
  background: #ffffff;
}

.menu {
  display: flex;
  gap: 0.8rem;
}

.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 1.2rem;
}

.auth-box {
  display: flex;
  gap: 0.6rem;
  align-items: center;
}
</style>
