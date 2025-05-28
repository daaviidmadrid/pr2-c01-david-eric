<script setup>
import { ref, onMounted } from "vue";
import { useAuthStore } from "../store/authStore";
import AuthService from "@/services/auth";

const authStore = useAuthStore();

const username = ref("");
const password = ref("");
const showRegisterModal = ref(false);

// Camps de registre
const regUsername = ref("");
const regEmail = ref("");
const regPassword = ref("");
const regPassword2 = ref("");
const registerError = ref(null);
const registerSuccess = ref(false);

onMounted(() => {
  authStore.initializeAuthStore();
  authStore.getAllPlayers();
});

const startGame = () => {
  window.location.href = "/game";
};

const authenticateUser = () => {
  if (!username.value || !password.value) {
    alert("Please enter both username and password.");
    return;
  }
  authStore.login({ username: username.value, password: password.value });
};

const logOut = () => {
  authStore.logout();
};

const handleRegister = async () => {
  registerError.value = null;
  registerSuccess.value = false;

  if (regPassword.value !== regPassword2.value) {
    registerError.value = "Les contrasenyes no coincideixen.";
    return;
  }

  try {
    await AuthService.register({
      username: regUsername.value,
      email: regEmail.value,
      password: regPassword.value,
      password2: regPassword2.value,
    });
    registerSuccess.value = true;
    // Neteja camps i tanca la modal
    regUsername.value = "";
    regEmail.value = "";
    regPassword.value = "";
    regPassword2.value = "";
    showRegisterModal.value = false;
  } catch (err) {
    registerError.value =
      err.response?.data?.detail || "Error en el registre. Comprova les dades.";
  }
};
</script>

<template>
  <div class="home text-center mt-4">
    <h1>Welcome to Battleship Game</h1>

    <div v-if="authStore.isAuthenticated" class="mt-5">
      <h3>You're logged in!</h3>
      <div class="mb-3">
        Access Token: {{ authStore.accessToken.slice(0, 20) }}...
      </div>
      <button class="btn btn-primary mr-2" @click="startGame">
        Start New Game
      </button>
      <button class="btn btn-secondary" @click="logOut">Log Out</button>
    </div>

    <div v-else>
      <h3>Please log in to play</h3>
      <form
        @submit.prevent="authenticateUser"
        class="mx-auto"
        style="max-width: 300px"
      >
        <input
          v-model="username"
          type="text"
          placeholder="Username"
          class="form-control mb-2"
        />
        <input
          v-model="password"
          type="password"
          placeholder="Password"
          class="form-control mb-2"
        />
        <button class="btn btn-primary w-100" :disabled="authStore.loading">
          {{ authStore.loading ? "Logging in..." : "Log In" }}
        </button>
        <div v-if="authStore.error" class="text-danger mt-2">
          {{ authStore.error }}
        </div>
      </form>

      <button class="btn btn-link mt-2" @click="showRegisterModal = true">
        No tens compte? Registra't
      </button>
    </div>

    <div v-if="authStore.playersList.length > 0" class="mt-5">
      <h3>Jugadors disponibles</h3>
      <ul class="list-group">
        <li
          v-for="player in authStore.playersList"
          :key="player.id"
          class="list-group-item"
        >
          {{ player.nickname }}
        </li>
      </ul>
    </div>

  </div>
  <!-- Modal de registre -->
  <div
    v-if="showRegisterModal"
    class="modal d-block"
    tabindex="-1"
    style="background: rgba(0, 0, 0, 0.5)"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content p-4">
        <h5 class="modal-title">Registre d'usuari</h5>
        <input v-model="regUsername" class="form-control my-2" placeholder="Nom d'usuari" />
        <input v-model="regEmail" class="form-control my-2" placeholder="Correu electrònic" type="email" />
        <input v-model="regPassword" class="form-control my-2" placeholder="Contrasenya" type="password" />
        <input v-model="regPassword2" class="form-control my-2" placeholder="Confirma la contrasenya" type="password" />

        <div v-if="registerError" class="text-danger mt-2">{{ registerError }}</div>
        <div v-if="registerSuccess" class="text-success mt-2">Registre complet! Ja pots iniciar sessió.</div>

        <div class="d-flex justify-content-between mt-3">
          <button class="btn btn-primary" @click="handleRegister">Registra't</button>
          <button class="btn btn-secondary" @click="showRegisterModal = false">Tancar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  max-width: 600px;
  margin: 0 auto;
}

.modal-content {
  border-radius: 10px;
  background-color: #fff;
}
</style>
