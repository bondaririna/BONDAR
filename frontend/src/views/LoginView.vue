<script setup>
import { nextTick, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

const form = reactive({
  username: '',
  password: '',
})

const googleContainer = ref(null)
const googleReady = ref(false)
const googleError = ref('')

async function onSubmit() {
  try {
    await auth.loginWithPassword(form.username, form.password)
    router.push('/events')
  } catch {
    // Error text is already exposed from the store.
  }
}

function initGoogleButton() {
  const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID
  if (!clientId) {
    googleError.value = 'Lipseste VITE_GOOGLE_CLIENT_ID in .env'
    return
  }
  if (!window.google?.accounts?.id || !googleContainer.value) {
    googleError.value = 'Google OAuth nu este disponibil momentan.'
    return
  }

  googleError.value = ''
  window.google.accounts.id.initialize({
    client_id: clientId,
    callback: async (response) => {
      if (!response.credential) {
        googleError.value = 'Nu am primit credential Google.'
        return
      }
      try {
        await auth.loginWithGoogleIdToken(response.credential)
        router.push('/events')
      } catch {
        // Error text is managed in auth store.
      }
    },
  })
  window.google.accounts.id.renderButton(googleContainer.value, {
    theme: 'outline',
    size: 'large',
    shape: 'pill',
    text: 'signin_with',
  })
  googleReady.value = true
}

onMounted(async () => {
  await nextTick()
  if (window.google?.accounts?.id) {
    initGoogleButton()
    return
  }

  const script = document.createElement('script')
  script.src = 'https://accounts.google.com/gsi/client'
  script.async = true
  script.defer = true
  script.onload = () => initGoogleButton()
  script.onerror = () => {
    googleError.value = 'Nu pot incarca scriptul Google OAuth.'
  }
  document.head.appendChild(script)
})
</script>

<template>
  <div class="login-layout">
    <section class="card hero">
      <p class="pill">Acces securizat</p>
      <h2>Intră în cont pentru a continua</h2>
      <p class="muted">
        Studenți: Google Sign-In @student.usv.ro pentru funcționalitățile critice (feedback, înscriere).
        Organizatori/Admin: autentificare cu user/parolă pentru gestionare evenimente și validare.
      </p>
      <ul>
        <li>Protecție cu token Bearer</li>
        <li>Roluri: student / organizer / admin</li>
        <li>Acces diferențiat la rute și acțiuni</li>
      </ul>
    </section>

    <section class="card login-card">
      <h3>Autentificare Google (student)</h3>
      <div ref="googleContainer" class="google-button-wrap" />
      <p v-if="!googleReady && !googleError">Se încarcă Google Sign-In...</p>
      <p v-if="googleError" class="error">{{ googleError }}</p>
      <p v-if="auth.error && !googleError" class="error">{{ auth.error }}</p>
    </section>

    <section class="card login-card">
      <h3>Autentificare cu parolă (organizer/admin)</h3>
      <form @submit.prevent="onSubmit">
        <div class="form-row">
          <label for="username">Email</label>
          <input id="username" v-model="form.username" type="email" required placeholder="ex: organizator@usv.ro" />
        </div>
        <div class="form-row">
          <label for="password">Parola</label>
          <input id="password" v-model="form.password" type="password" required />
        </div>
        <p v-if="auth.error" class="error">{{ auth.error }}</p>
        <button class="btn" type="submit" :disabled="auth.loading">
          {{ auth.loading ? 'Se autentifică...' : 'Login' }}
        </button>
      </form>
    </section>
  </div>
</template>

<style scoped>
.login-layout {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 420px));
  gap: 1rem;
  align-items: start;
}

.hero {
  grid-column: 1 / -1;
  background: radial-gradient(circle at 25% 20%, #e8f1ff 0, #fff 35%), #fff;
}

.hero ul {
  margin: 0.6rem 0 0;
  padding-left: 1.1rem;
  color: #3d4a5f;
  display: grid;
  gap: 0.25rem;
}

.login-card {
  width: 100%;
}

.google-button-wrap {
  display: flex;
  justify-content: center;
  margin: 0.75rem 0;
}
</style>
