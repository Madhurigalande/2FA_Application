<template>
  <div class="container">
    <div class="form-card">
      <h2>Login</h2>

      <transition name="slide-fade" mode="out-in">
        <div v-if="!show2FA" key="login">
          <input
            v-model="username"
            placeholder="Enter Username"
            @input="clearMessage"
          />
          <input
            v-model="password"
            type="password"
            placeholder="Enter Password"
            @input="clearMessage"
          />
          <button @click="login" :disabled="loading">
            {{ loading ? "Logging in..." : "Login" }}
          </button>
        </div>

        <div v-else key="2fa">
          <h3>Enter 2FA Code</h3>
          <input
            v-model="code"
            placeholder="6-digit code"
            maxlength="6"
            @input="clearMessage"
          />
          <button @click="verify2FA" :disabled="loading">
            {{ loading ? "Verifying..." : "Verify" }}
          </button>
        </div>
      </transition>

      <transition name="fade">
        <p v-if="message" :class="statusClass">{{ message }}</p>
      </transition>

      <p class="link">
        Don’t have an account?
        <router-link to="/register">Register</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, computed } from "vue";
import { useRouter } from "vue-router";

const username = ref("");
const password = ref("");
const code = ref("");
const message = ref("");
const show2FA = ref(false);
const loading = ref(false);
const status = ref("");
const router = useRouter();

const statusClass = computed(() =>
  status.value === "success" ? "success" : "error"
);

const clearMessage = () => {
  message.value = "";
};

const login = async () => {
  if (!username.value || !password.value) {
    message.value = "Please enter both username and password";
    status.value = "error";
    return;
  }
  try {
    loading.value = true;
    const res = await axios.post("http://localhost:8000/login", {
      username: username.value,
      password: password.value,
    });

    if (res.data?.["2fa_required"]) {
      show2FA.value = true;
      message.value = "2FA required — check your authenticator app.";
      status.value = "success";
    } else {
      message.value = "Login successful!";
      status.value = "success";
      localStorage.setItem("user", username.value);
      router.push("/dashboard");
    }
  } catch (err) {
    message.value = err.response?.data?.detail || "Login failed";
    status.value = "error";
  } finally {
    loading.value = false;
  }
};

const verify2FA = async () => {
  if (!code.value) {
    message.value = "Please enter your 2FA code";
    status.value = "error";
    return;
  }

  try {
    loading.value = true;
    const res = await axios.post("http://localhost:8000/verify-2fa", {
      username: username.value,
      code: code.value,
    });
    message.value = res.data.message || "2FA verified successfully!";
    status.value = "success";
    localStorage.setItem("user", username.value);
    router.push("/dashboard");
  } catch (err) {
    message.value = err.response?.data?.detail || "Invalid 2FA code";
    status.value = "error";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* Background */
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #a5d8ff, #d6ecff);
  font-family: "Poppins", sans-serif;
}

/* Card Layout */
.form-card {
  background: #ffffff;
  padding: 2.5rem;
  border-radius: 18px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  width: 360px;
  text-align: center;
  transition: all 0.3s ease;
}

.form-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

h2 {
  color: #0078d4;
  margin-bottom: 1rem;
}

/* Inputs */
input {
  width: 90%;
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 15px;
  transition: 0.2s;
}

input:focus {
  outline: none;
  border-color: #0078d4;
  box-shadow: 0 0 5px #0078d4;
}

/* Buttons */
button {
  padding: 10px 20px;
  margin-top: 12px;
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
  background-color: #a3c9eb;
  cursor: not-allowed;
}

/* Links */
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

/* Messages */
.success {
  color: #0c7c0c;
  margin-top: 1rem;
}

.error {
  color: #d00000;
  margin-top: 1rem;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-fade-enter-active {
  transition: all 0.5s ease;
}
.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
</style>
