<template>
  <div class="container">
    <h2>Welcome, {{ username }}</h2>
    <p>This is your dashboard.</p>

    <button @click="goTo2FA">Enable 2FA</button>
    <button @click="logout">Logout</button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'

const router = useRouter()
const username = ref('')

onMounted(() => {
  const user = localStorage.getItem('user')
  if (!user) router.push('/login')
  else username.value = user
})

const goTo2FA = () => router.push('/enable-2fa')
const logout = () => {
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.container {
  max-width: 400px;
  margin: 100px auto;
  text-align: center;
  background: white;
  padding: 2rem;
  border-radius: 10px;
}
button {
  margin: 10px;
  padding: 10px 20px;
  border: none;
  background: #0078d4;
  color: white;
  border-radius: 6px;
}
</style>
