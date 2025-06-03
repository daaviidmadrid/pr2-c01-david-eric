<script setup>
import { onMounted, onUnmounted } from "vue";
import { useGameStore } from "../store";
import { useAuthStore } from "../store/authStore";
import GameBoard from "../components/GameBoard.vue";
import DockingArea from "../components/DockingArea.vue";

const store = useGameStore();
const authStore = useAuthStore();

const refreshGameState = async () => {
  if (store.gameId) {
    await store.getGameState(store.gameId);
  }
};

let intervalId = null;

onMounted(async () => {
  await store.startNewGame();
  intervalId = setInterval(refreshGameState, 5000); // refresc cada 5s
});

onUnmounted(() => {
  clearInterval(intervalId);
});

const onLogout = () => {
  if (confirm("Are you sure you want to log out?")) {
    authStore.logout();
    window.location.href = "/";
  }
};
</script>

<template>
  <div class="container-fluid">
    <h1 class="text-center my-2">
      Battleship (Hello: {{ authStore.username }})
      <button class="btn btn-sm btn-outline-danger ms-2" @click="onLogout">
        Logout
      </button>
    </h1>

    <!-- Game Info Panel -->
    <div class="row mb-3">
      <div class="col text-center">
        <h4>Game Info</h4>
        <ul class="list-unstyled">
          <li><strong>Game ID:</strong> {{ store.gameId }}</li>
          <li><strong>Phase:</strong> {{ store.gamePhase }}</li>
          <li><strong>Turn:</strong> {{ String(store.turn) }}</li>
          <li><strong>Winner:</strong> {{ String(store.winner) }}</li>
        </ul>
      </div>
    </div>

    <div class="row">
      <!-- Player Board -->
      <div class="col-lg-5 d-flex flex-column align-items-center">
        <h3 class="text-center">Your Fleet</h3>
        <GameBoard
          :board="store.playerBoard"
          :ships="store.playerPlacedShips"
          @cell-click="store.handlePlayerBoardClick"
        />
      </div>

      <!-- Docking or Status -->
      <div class="col-lg-2 d-flex flex-column justify-content-center">
        <div class="game-controls text-center">
          <div class="game-status mb-3">{{ store.gameStatus }}</div>
          <button class="btn btn-primary" @click="store.startNewGame()">
            New Game
          </button>
        </div>

        <DockingArea
          v-if="store.gamePhase === 'placement'"
          :ships="store.availableShips"
          @ship-selected="store.selectShip"
          @rotate-ship="store.rotateSelectedShip"
        />
      </div>

      <!-- Opponent Board -->
      <div class="col-lg-5 d-flex flex-column align-items-center">
        <h3 class="text-center">Enemy Fleet</h3>
        <GameBoard
          :board="store.opponentBoard"
          :ships="store.opponentShips"
          :hidden="true"
          @cell-click="store.handleOpponentBoardClick"
        />
      </div>
    </div>

    <!-- JSON Debug Info -->
    <div class="row mt-4">
      <div class="col-12">
        <h4 class="text-center">Debug Info (Game State)</h4>
        <pre class="text-start small bg-light p-2 border rounded" style="max-height: 300px; overflow-y: auto;">
{{ JSON.stringify({
  playerId: store.playerId,
  opponentId: store.opponentId,
  availableShips: store.availableShips,
  placedShips: store.playerPlacedShips,
  opponentShips: store.opponentShips,
  playerBoard: store.playerBoard,
  opponentBoard: store.opponentBoard
}, null, 2) }}
        </pre>
      </div>
    </div>
  </div>
</template>

<style>
.game-controls {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin: 20px 0;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}
.game-status {
  font-size: 1.2rem;
  font-weight: bold;
}
</style>