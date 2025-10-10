<template>
  <div class="container">
    <div class="form-card">
      <h2>Register</h2>

      <input
        v-model="username"
        placeholder="Enter Username"
        @input="clearMessage"
      />
      <input
        v-model="password"
        placeholder="Enter Password"
        type="password"
        @input="clearMessage"
      />

      <button @click="register" :disabled="loading">
        {{ loading ? "Registering..." : "Register" }}
      </button>

      <p class="link">
        Already have an account?
        <router-link to="/login">Login</router-link>
      </p>

      <transition name="fade">
        <p v-if="message" :class="statusClass">{{ message }}</p>
      </transition>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, computed } from "vue";

const username = ref("");
const password = ref("");
const message = ref("");
const status = ref(""); // 'success' or 'error'
const loading = ref(false);

const statusClass = computed(() =>
  status.value === "success" ? "success" : "error"
);

const clearMessage = () => {
  message.value = "";
};

const register = async () => {
  if (!username.value || !password.value) {
    message.value = "Please fill out all fields";
    status.value = "error";
    return;
  }

  try {
    loading.value = true;
    const res = await axios.post("http://localhost:8000/register", {
      username: username.value,
      password: password.value,
    });
    message.value = res.data.message || "Registration successful!";
    status.value = "success";
    username.value = "";
    password.value = "";
  } catch (err) {
    message.value = err.response?.data?.detail || "Registration failed";
    status.value = "error";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #c7e6ff, #e1f3ff);
  font-family: "Poppins", sans-serif;
}

.form-card {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
  width: 350px;
  text-align: center;
  transition: all 0.3s ease;
}

.form-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
}

h2 {
  color: #0078d4;
  margin-bottom: 1rem;
}

input {
  width: 90%;
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #c8c8c8;
  border-radius: 6px;
  font-size: 15px;
  transition: 0.2s;
}

input:focus {
  outline: none;
  border-color: #0078d4;
  box-shadow: 0 0 4px #0078d4;
}

button {
  padding: 10px 20px;
  margin-top: 10px;
  background-color: #0078d4;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  width: 100%;
  font-weight: 500;
  transition: background-color 0.3s, transform 0.2s;
}

button:hover {
  background-color: #005fa3;
  transform: scale(1.03);
}

button:disabled {
  background-color: #a1c8eb;
  cursor: not-allowed;
}

.link {
  margin-top: 1rem;
  color: #555;
  font-size: 14px;
}

.link a {
  color: #0078d4;
  text-decoration: none;
  font-weight: 500;
}

.link a:hover {
  text-decoration: underline;
}

.success {
  color: #0c7c0c;
  font-weight: 500;
}

.error {
  color: #c40000;
  font-weight: 500;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
