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
    <section class="card login-card">
      <h2>Autentificare Google)</h2>
      <div ref="googleContainer" class="google-button-wrap" />
      <p v-if="!googleReady && !googleError">Se incarca Google Sign-In...</p>
      <p v-if="googleError" class="error">{{ googleError }}</p>
      <p v-if="auth.error" class="error">{{ auth.error }}</p>
    </section>

    <section class="card login-card">
      <h2>Autentificare</h2>
      <form @submit.prevent="onSubmit">
        <div class="form-row">
          <label for="username">Email</label>
          <input id="username" v-model="form.username" type="email" required />
        </div>
        <div class="form-row">
          <label for="password">Parola</label>
          <input id="password" v-model="form.password" type="password" required />
        </div>
        <p v-if="auth.error" class="error">{{ auth.error }}</p>
        <button class="btn" type="submit" :disabled="auth.loading">
          {{ auth.loading ? 'Se autentifica...' : 'Login' }}
        </button>
      </form>
    </section>
  </div>
</template>

<style scoped>
.login-layout {
  min-height: calc(100vh - 180px);
  display: grid;
  grid-template-columns: repeat(2, minmax(320px, 460px));
  justify-content: center;
  align-content: center;
  gap: 1rem;
}

.login-card {
  width: 100%;
}

.google-button-wrap {
  display: flex;
  justify-content: center;
  margin: 0.75rem 0;
}

@media (max-width: 900px) {
  .login-layout {
    min-height: auto;
    grid-template-columns: minmax(280px, 520px);
    align-content: start;
  }
}
</style>
