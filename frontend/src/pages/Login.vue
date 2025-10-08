<template>
  <div class="container">
    <h2>Login</h2>

    <div v-if="!show2FA">
      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <button @click="login">Login</button>
    </div>

    <div v-else>
      <h3>Enter 2FA Code</h3>
      <input v-model="code" placeholder="6-digit code" />
      <button @click="verify2FA">Verify</button>
    </div>

    <p>{{ message }}</p>
    <p>Don't have an account? <router-link to="/register">Register</router-link></p>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const code = ref('')
const message = ref('')
const show2FA = ref(false)
const router = useRouter()

const login = async () => {
  try {
    const res = await axios.post('http://localhost:8000/login', {
      username: username.value,
      password: password.value
    })
    if (res.data?.['2fa_required']) {
      show2FA.value = true
    } else {
      localStorage.setItem('user', username.value)
      router.push('/dashboard')
    }
  } catch (err) {
    message.value = err.response?.data?.detail || 'Login failed'
  }
}

const verify2FA = async () => {
  try {
    const res = await axios.post('http://localhost:8000/verify-2fa', {
      username: username.value,
      code: code.value
    })
    message.value = res.data.message
    localStorage.setItem('user', username.value)
    router.push('/dashboard')
  } catch (err) {
    message.value = err.response?.data?.detail || 'Invalid 2FA code'
  }
}
</script>

<style scoped>
.container {
  max-width: 400px;
  margin: 100px auto;
  padding: 2rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px #ccc;
  text-align: center;
}
input {
  width: 90%;
  margin: 10px 0;
  padding: 10px;
}
button {
  padding: 10px 20px;
  background-color: #0078d4;
  color: white;
  border: none;
  border-radius: 6px;
}
</style>
