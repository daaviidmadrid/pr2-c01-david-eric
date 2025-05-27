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
    return Promise.resolve(
      JSON.stringify({
        status: 200,
        message: "OK",
        data: {
          gameState: {
            gameId: "12345",
            phase: "playing", // "placement", "playing", "gameOver"
            turn: "player1",
            winner: null,
            player1: {
              id: "1",
              username: "admin",
              placedShips: [
                {
                  type: 1,
                  position: { row: 1, col: 3 },
                  isVertical: true,
                  size: 1,
                },
                {
                  type: 2,
                  position: { row: 3, col: 4 },
                  isVertical: false,
                  size: 2,
                },
                {
                  type: 3,
                  position: { row: 5, col: 2 },
                  isVertical: true,
                  size: 3,
                },
                {
                  type: 4,
                  position: { row: 6, col: 7 },
                  isVertical: false,
                  size: 4,
                },
                {
                  type: 5,
                  position: { row: 1, col: 8 },
                  isVertical: true,
                  size: 5,
                },
              ],
              availableShips: [],
              board: [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 11, 0, 1, 0, 0, 0, 0, 5, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                [0, 0, 0, 2, 2, 0, 0, 0, 5, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                [0, 0, -3, 0, 0, 0, 0, 0, 5, 0],
                [0, 0, 3, 0, 4, -4, 4, 4, 0, 0],
                [0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 11, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              ],
            },
            player2: {
              id: "2",
              username: "player2",
              placedShips: [
                {
                  type: 1,
                  position: { row: 1, col: 3 },
                  isVertical: true,
                  size: 1,
                },
                {
                  type: 2,
                  position: { row: 3, col: 4 },
                  isVertical: false,
                  size: 2,
                },
                {
                  type: 3,
                  position: { row: 5, col: 2 },
                  isVertical: true,
                  size: 3,
                },
                {
                  type: 4,
                  position: { row: 6, col: 7 },
                  isVertical: false,
                  size: 4,
                },
                {
                  type: 5,
                  position: { row: 1, col: 8 },
                  isVertical: true,
                  size: 5,
                },
              ],
              availableShips: [],
              board: [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 11, 0, 1, 0, 0, 0, 0, 5, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                [0, 0, 0, 2, 2, 0, 0, 0, 5, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                [0, 0, -3, 0, 0, 0, 0, 0, 5, 0],
                [0, 0, 3, 0, 4, -4, 4, 4, 0, 0],
                [0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 11, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              ],
            },
          },
        },
      })
    );
  },

  // async getGameState1(gameId) {
  //   // 1. Trae datos generales de la partida
  //   const { data: game } = await this.getGame(gameId);
  //
  //   // 2. Lista de jugadores en la partida
  //   const { data: players } = await this.getGamePlayers(gameId);
  //
  //   // 3. Construye el objeto gameState
  //   const gameState = {
  //     gameId: game.id,
  //     phase: game.phase,      // placement | playing | gameOver
  //     turn: game.turn,
  //     winner: game.winner     // o null
  //   };
  //
  //   // 4. Para cada jugador, recopila sus datos
  //   for (const p of players) {
  //     // 4.1 Info de usuario
  //     const { data: user } = await this.getUser(p.id);
  //     // 4.2 Barcos colocados
  //     const { data: vessels } = await this.getGamePlayerVessels(
  //       gameId,
  //       p.id
  //     );
  //     // 4.3 Barcos aún disponibles (si lo aporta tu API en game.availableShips)
  //     const availableShips = game.availableShips || [];
  //     // 4.4 Tableros (normalmente uno por jugador)
  //     const { data: boards } = await this.getGamePlayerBoards(
  //       gameId,
  //       p.id
  //     );
  //     // Selecciona el primer tablero, o crea uno vacío si no hay
  //     let boardGrid = Array.from({ length: 10 }, () =>
  //       Array(10).fill(0)
  //     );
  //     if (boards.length > 0) {
  //       const boardId = boards[0].id;
  //       const { data: board } = await this.getGamePlayerBoard(
  //         gameId,
  //         p.id,
  //         boardId
  //       );
  //       boardGrid = board.grid; // asume que tu API devuelve { grid: [...] }
  //     }
  //     // 4.5 Disparos realizados
  //     const { data: shots } = await this.getGamePlayerShots(
  //       gameId,
  //       p.id
  //     );
  //
  //     // 4.6 Ensambla sección del jugador
  //     gameState[player${p.id}] = {
  //       id: p.id,
  //       username: user.username,
  //       placedShips: vessels,
  //       availableShips,
  //       board: boardGrid,
  //       shots
  //     };
  //   }
  //
  //   // 5. Devuelve igual que el stub anterior
  //   return {
  //     status: 200,
  //     message: 'OK',
  //     data: { gameState }
  //   };
  // },

  getUser(id) {
    return axiosInstance.get(`/api/v1/user/${id}`);
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
  // getGame(gameId) {
  //   return axiosInstance.get(`/api/v1/games/${gameId}`);
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
