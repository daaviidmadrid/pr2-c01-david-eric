import { defineStore } from "pinia";
import api from "../services/api";
import { useAuthStore } from "./authStore";

export const useGameStore = defineStore("game", {
  state: () => ({
    playerId: null,
    opponentId: null,
    gameId: null,
    winner: null,
    turn: null,
    username: null,
    gamePhase: "placement",
    gameStatus: "Place your ships",
    playerBoard: [],
    opponentBoard: [],
    playerPlacedShips: [],
    opponentShips: [],
    availableShips: [],
    selectedShip: null,
  }),

  actions: {
    getUser(id) {
      return api
        .getUser(id)
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          const message = error.response?.data?.detail || error.message;
          throw new Error(message);
        });
    },

    async createGame(playerId) {
      return api.createGame(playerId);
    },

    async getGameState(gameId) {
      return api
        .getGameState(gameId)
        .then((response) => {
          console.log("response", response);

          const gameState = response.data?.game_state_response?.data?.gameState;
          if (!gameState) {
            throw new Error("Respuesta de gameState inválida");
          }

          this.playerId = gameState.player1.id;
          this.opponentId = gameState.player2.id;
          this.gameId = gameState.gameId;
          this.playerBoard = gameState.player1.board;
          this.opponentBoard = gameState.player2.board;
          this.playerPlacedShips = gameState.player1.placedShips;
          this.opponentShips = gameState.player2.placedShips;
          this.availableShips = gameState.player1.availableShips;
          this.gamePhase = gameState.phase;
          this.winner = gameState.winner;
          this.turn = gameState.turn;

          //this.gameStatus =
          //   gameState.turn === "player1" ? "Your turn" : "Opponent's turn";
          if (this.gamePhase === "playing") {
            this.gameStatus =
              gameState.turn === this.username ? "Your turn" : "Opponent's turn";
          } else if (this.gamePhase === "placement") {
            this.gameStatus = "Place your ships";
          } else if (this.gamePhase === "gameOver") {
            this.gameStatus = "Game Over - Winner " + gameState.winner;
          }
        })
        .catch((error) => {
          const message = error.response?.data?.detail || error.message;
          throw new Error(message);
        });
    },
    createEmptyBoard() {
      return Array(10)
        .fill()
        .map(() => Array(10).fill(0));
    },

    async startNewGame() {
      this.gamePhase = "placement";
      this.gameStatus = "Place your ships";
      this.playerBoard = this.createEmptyBoard();
      this.opponentBoard = this.createEmptyBoard();
      this.playerPlacedShips = [];
      this.opponentShips = [];
      this.selectedShip = null;
      this.availableShips = await api.getAvailableShips(); // TODO check with axios on how to avoid await.
      this.winner = null;


      try{
        const authStore = useAuthStore();
        authStore.initializeAuthStore();
        this.playerId = await authStore.getPlayer();
        this.username = authStore.username;
        if(!this.playerId) {
          throw new Error("Player ID is not set. Please log in first.");
        }
        const game = await this.createGame(this.playerId);
        console.log("Raw game object received:", game);
        console.log("Game started with ID:", game.id);
        this.gameId = game.id;
        await this.getGameState(this.gameId);

        this.availableShips = await api.getAvailableShips();
      } catch (error) {
        console.error("Error starting new game:", error);
        throw error;
      }

      this.placeOpponentShips();
      return
    },

    addVessel(gameId, playerId, vessel) {
        return api
            .addVessel(gameId, playerId, vessel)
            .then((response) => {
            console.log("Vessel added:", response.data);
            return response.data;
            })
            .catch((error) => {
            const message = error.response?.data?.detail || error.message;
            throw new Error(message);
            });
    },

    addPlayerGameShot(gameId, playerId, shotData) {
        return api
            .addPlayerGameShot(gameId, playerId, shotData)
            .then((response) => {
            console.log("Shot added:", response.data);
            return response.data;
            })
            .catch((error) => {
            const message = error.response?.data?.detail || error.message;
            throw new Error(message);
            });
    },

    placeShip(board, row, col, size, isVertical, type) {
      for (let i = 0; i < size; i++) {
        const r = isVertical ? row + i : row;
        const c = isVertical ? col : col - i;
        board[r][c] = type;
      }
    },

    isValidPlacement(board, row, col, size, isVertical) {
      const inBounds = isVertical ? row + size <= 10 : col + 1 - size >= 0;
      if (!inBounds) return false;

      for (let i = 0; i < size; i++) {
        const r = isVertical ? row + i : row;
        const c = isVertical ? col : col - i;
        if (board[r][c] !== 0) return false;
      }
      return true;
    },

    placeOpponentShips() {
      const shipList = [1, 2, 3, 4, 5];
      for (let type of shipList) {
        const ship = this.availableShips.find((s) => s.type === type);
        let placed = false;
        while (!placed) {
          const row = Math.floor(Math.random() * 10);
          const col = Math.floor(Math.random() * 10);
          const isVertical = Math.random() > 0.5;
          if (
            this.isValidPlacement(
              this.opponentBoard,
              row,
              col,
              ship.size,
              isVertical
            )
          ) {
            this.placeShip(
              this.opponentBoard,
              row,
              col,
              ship.size,
              isVertical,
              ship.type
            );
            this.opponentShips.push({
              ...ship,
              isVertical,
              position: { row, col },
            });
            placed = true;
          }
        }
      }
    },

    selectShip(ship) {
      this.selectedShip = { ...ship };
    },

    rotateSelectedShip() {
      if (this.selectedShip) {
        this.selectedShip.isVertical = !this.selectedShip.isVertical;
      }
    },

    async handlePlayerBoardClick(row, col) {
      if (this.gamePhase !== "placement" || !this.selectedShip || this.availableShips.length === 0) return;

      const ship = this.selectedShip;
      if (!this.isValidPlacement(this.playerBoard, row, col, ship.size, ship.isVertical)) return;

      this.placeShip(this.playerBoard, row, col, ship.size, ship.isVertical, ship.type);
      this.playerPlacedShips.push({ ...ship, position: { row, col } });

      console.log("Añadiendo barco a:", this.gameId, this.playerId);

      try {
        await api.addVessel(this.gameId, this.playerId, {
          type: ship.type,
          x: row,
          y: col,
          isVertical: ship.isVertical,
        });

        await this.getGameState(this.gameId);
      } catch (error) {
        console.error("Error enviando barco al backend:", error);
      }

      this.availableShips = this.availableShips.filter((s) => s.type !== ship.type);
      this.selectedShip = null;

      if (this.availableShips.length === 0) {
        this.gamePhase = "playing";
        this.gameStatus = "Your turn";
      }
    },

    async handleOpponentBoardClick(row, col) {
      if (this.gamePhase !== "playing") return;

      try {
        await api.addPlayerGameShot(this.gameId, this.playerId, { x: row, y: col });

        // Refresca estado tras el disparo del jugador y del bot
        await this.getGameState(this.gameId);

        if (this.gamePhase === "gameOver") {
          this.gameStatus = "Game Over - Winner " + this.winner;
        } else if (this.gamePhase === "playing") {
          // 💡 Aquí comprobamos si es un solo jugador
          this.gameStatus = "Your turn";
        }

      } catch (error) {
        const detail = error.response?.data?.detail;
        this.gameStatus = "Error al disparar" + (detail ? `: ${detail}` : ".");
        console.error(error);
      }
    },
  },
});
