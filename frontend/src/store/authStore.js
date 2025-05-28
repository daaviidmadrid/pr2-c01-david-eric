import { defineStore } from "pinia";
import AuthService from "../services/auth";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    username: null,
    accessToken: null,
    refreshToken: null,
    isAuthenticated: false,
    loading: false,
    error: null,
    playersList: [],
  }),
  actions: {
    async getAllPlayers() {
      console.log("Token", this.accessToken);
      try {
        const response = await AuthService.getAllPlayers();
        for (const player of response.data) {
          this.playersList.push({
            id: player.id,
            nickname: player.nickname,
          });
        }
      } catch (error) {
        const message = error.response?.data?.detail || error.message;
        throw new Error(message);
      }
    },
    initializeAuthStore() {
      this.username = localStorage.getItem("username");
      this.accessToken = localStorage.getItem("access");
      this.refreshToken = localStorage.getItem("refresh");
      this.isAuthenticated = !!this.accessToken;
    },
    login(user) {
      this.loading = true;
      this.error = null;

      return AuthService.login(user)
      .then((response) => {
          console.log("response", response);
          // response = JSON.parse(response); // això era una simulació, en el cas real és una resposta d'axios i podem comentar aquesta línia
          this.username = user.username;
          this.accessToken = response.data.access;
          this.refreshToken = response.data.refresh;
          this.isAuthenticated = true;

          localStorage.setItem("username", this.username);
          localStorage.setItem("access", this.accessToken);
          localStorage.setItem("refresh", this.refreshToken);
      })
      .catch((error) => {
          console.log("error", error);
          this.error =
          error.response?.data?.detail || "Error d'inici de sessió. Torna-ho a intentar.";
          this.isAuthenticated = false;
      })
      .finally(() => {
          this.loading = false;
      });
    },

    logout() {
      this.accessToken = null;
      this.refreshToken = null;
      this.isAuthenticated = false;
      localStorage.removeItem("username");
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
    },
  },
});
