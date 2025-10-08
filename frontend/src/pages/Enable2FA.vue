<template>
  <div class="container">
    <h2>Enable Two-Factor Authentication</h2>

    <div v-if="!qrCode">
      <button @click="enable2FA">Generate QR Code</button>
    </div>

    <div v-else>
      <p>Scan this QR code with your authenticator app:</p>
      <img :src="'data:image/png;base64,' + qrCode" width="200" />
      <p><router-link to="/dashboard">Back to Dashboard</router-link></p>
    </div>

    <p>{{ message }}</p>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'

const qrCode = ref('')
const message = ref('')

const enable2FA = async () => {
  const username = localStorage.getItem('user')
  if (!username) {
    message.value = 'User not logged in'
    return
  }

  try {
    const res = await axios.post(`http://localhost:8000/enable-2fa/${username}`)
    qrCode.value = res.data.qr_code
  } catch (err) {
    message.value = err.response?.data?.detail || 'Error enabling 2FA'
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
  text-align: center;
  box-shadow: 0 2px 8px #ccc;
}
button {
  padding: 10px 20px;
  background-color: #0078d4;
  color: white;
  border: none;
  border-radius: 6px;
}
</style>
