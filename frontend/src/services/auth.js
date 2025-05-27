import axios from "axios";

class AuthService {
  login(user) {
    return axios.post("/api/token/", {
      username: user.username,
      password: user.password,
    });
  }

  refresh(refreshToken) {
    return Promise.resolve(
      JSON.stringify({
        access: "mockAccessToken",
      })
    );
  }

  logout() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
  }

  getAccessToken() {
    return localStorage.getItem("access");
  }

  getRefreshToken() {
    return localStorage.getItem("refresh");
  }

  isLoggedIn() {
    return !!localStorage.getItem("access");
  }

  getAxiosInstance() {
    const apiUrl = import.meta.env.VITE_API_URL;
    const instance = axios.create({
      baseURL: apiUrl,
      headers: {
        Authorization: `Bearer ${this.getAccessToken()}`,
      },
    });

    instance.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response.status === 401 && this.isLoggedIn()) {
          try {
            const response = await this.refresh(this.getRefreshToken());
            localStorage.setItem("access", response.data.access);
            error.config.headers["Authorization"] =
              "Bearer " + response.data.access;
            return axios.request(error.config);
          } catch (err) {
            this.logout();
          }
        }
        return Promise.reject(error);
      }
    );

    return instance;
  }
  getAllPlayers() {
    return this.getAxiosInstance().get("/api/v1/players/");
  }
  //
  // getPlayer(id) {
  //     return this.getAxiosInstance().get(`/api/v1/players/${id}/`);
  // }
  //
  // putPlayer(id, data) {
  //     return this.getAxiosInstance().put(`/api/v1/players/${id}/`, data);
  // }
  //
  // patchPlayer(id, data) {
  //     return this.getAxiosInstance().patch(`/api/v1/players/${id}/`, data);
  // }
  //
  // deletePlayer(id) {
  //     return this.getAxiosInstance().delete(`/api/v1/players/${id}/`);
  // }
}

export default new AuthService();
