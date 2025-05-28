import AuthService from "@/services/auth.js";
const axiosInstance = AuthService.getAxiosInstance();

export default {
  getAvailableShips() {
    return Promise.resolve([
      {
        type: 1,
        isVertical: true,
        size: 1,
      },
      {
        type: 2,
        isVertical: true,
        size: 2,
      },
      {
        type: 3,
        isVertical: true,
        size: 3,
      },
      {
        type: 4,
        isVertical: true,
        size: 4,
      },
      {
        type: 5,
        isVertical: true,
        size: 5,
      },
    ]);
  },

  getGameState(gameId) {
    return axiosInstance
      .get(`/api/v1/games/${gameId}/`)
      .then((response) => {
        // Si el backend ya devuelve el objeto en el formato correcto:
        return response.data;
        // Si necesitas adaptar el formato, puedes hacerlo aquí antes de retornarlo.
      });
  },

  getUser(id) {
    return axiosInstance.get(`/api/v1/user/${id}`);
  },

  getGame(gameId) {
    return axiosInstance.get(`/api/v1/games/${gameId}`);
  },

  //
  // getAllGames() {
  //   return axiosInstance.get('/api/v1/games/');
  // },
  //
  // createGame() {
  //   return axiosInstance.post('/api/v1/games/');
  // },
  //
  // putGame(gameId, data) {
  //   return axiosInstance.put(`/api/v1/games/${gameId}/`, {data});
  // },
  //
  // patchGame(gameId, data) {
  //   return axiosInstance.patch(`/api/v1/games/${gameId}/`, {data});
  // },
  //
  // deleteGame(gameId) {
  //   return axiosInstance.delete(`/api/v1/games/${gameId}/`);
  // },
  //
  // getGamePlayers(gameId) {
  //   return axiosInstance.get(`/api/v1/games/${gameId}/players/`);
  // },
  //
  // addPlayerToGame(gameId, playerId) {
  //   return axiosInstance.post(`/api/v1/games/${gameId}/players/`, { playerId });
  // },
  //
  // getGamePlayer(gameId, playerId) {
  //   return axiosInstance.get(`/api/v1/games/${gameId}/players/${playerId}/`);
  // },
  //
  // deleteGamePlayer(gameId, playerId) {
  //   return axiosInstance.delete(`/api/v1/games/${gameId}/players/${playerId}/`);
  // },
  //
  // getGamePlayerVessels(gameId, playerId) {
  //   return axiosInstance.get(`/api/v1/games/${gameId}/players/${playerId}/vessels/`);
  // },
  //
  // addVesselToGamePlayer(gameId, playerId, vesselData) {
  //   return axiosInstance.post(`/api/v1/games/${gameId}/players/${playerId}/vessels/`, {vesselData});
  // },
  //
  // getGamePlayerVessel(gameId, playerId, vesselId) {
  //   return axiosInstance.get(`/api/v1/games/${gameId}/players/${playerId}/vessels/${vesselId}/`);
  // },
  //
  // putGamePlayerVessel(gameId, playerId, vesselId, vesselData) {
  //     return axiosInstance.put(`/api/v1/games/${gameId}/players/${playerId}/vessels/${vesselId}/`, {vesselData});
  // },
  //
  // patchGamePlayerVessel(gameId, playerId, vesselId, vesselData) {
  //   return axiosInstance.patch(`/api/v1/games/${gameId}/players/${playerId}/vessels/${vesselId}/`, {vesselData});
  // },
  //
  // deleteGamePlayerVessel(gameId, playerId, vesselId) {
  //     return axiosInstance.delete(`/api/v1/games/${gameId}/players/${playerId}/vessels/${vesselId}/`);
  // },
  //
  // getGamePlayerShots(gameId, playerId) {
  //   return axiosInstance.get(`/api/v1/games/${gameId}/players/${playerId}/shots/`);
  // },
  //
  // addGamePlayerShot(gameId, playerId, shotData) {
  //   return axiosInstance.post(`/api/v1/games/${gameId}/players/${playerId}/shots/`, {shotData});
  // },
  //
  // getGamePlayerShot(gameId, playerId, shotId) {
  //     return axiosInstance.get(`/api/v1/games/${gameId}/players/${playerId}/shots/${shotId}/`);
  // },
  //
  // getGamePlayerBoards(gameId, playerId) {
  //   return axiosInstance.get(`/api/v1/games/${gameId}/players/${playerId}/boards/`);
  // },
  //
  // getGamePlayerBoard(gameId, playerId, boardId) {
  //     return axiosInstance.get(`/api/v1/games/${gameId}/players/${playerId}/boards/${boardId}/`);
  // },
};
