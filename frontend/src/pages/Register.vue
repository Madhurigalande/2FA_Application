<template>
  <div class="container">
    <h2>Register</h2>
    <input v-model="username" placeholder="Username" />
    <input v-model="password" placeholder="Password" type="password"  />

    <button @click="register">Register</button>
    <p>Already have an account? <router-link to="/login">Login</router-link></p>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'

const username = ref('')
const password = ref('')
const message = ref('')

const register = async () => {
  try {
    const res = await axios.post('http://localhost:8000/register', {
      username: username.value,
      password: password.value
    })
    message.value = res.data.message
  } catch (err) {
    message.value = err.response?.data?.detail || 'Registration failed'
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
