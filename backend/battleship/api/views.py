from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, OpenApiParameter
import random

def seed_vessels():
    from .models import Vessel

    vessels_data = [
        (1, "Patrol Boat", 1),
        (2, "Destroyer", 2),
        (3, "Cruiser", 3),
        (4, "Submarine", 4),
        (5, "Carrier", 5),
    ]

    for vessel_id, name, size in vessels_data:
        Vessel.objects.get_or_create(
            id=vessel_id,
            defaults={
                "size": size,
                "name": name,
                "image": "placeholder.png"
            }
        )

def place_bot_ships(board):
    vessels = list(Vessel.objects.all())
    size = board.game.width

    occupied = set()

    for vessel in vessels:
        placed = False
        while not placed:
            is_vertical = random.choice([True, False])
            if is_vertical:
                row = random.randint(0, size - vessel.size)
                col = random.randint(0, size - 1)
                positions = [(row + i, col) for i in range(vessel.size)]
            else:
                row = random.randint(0, size - 1)
                col = random.randint(0, size - vessel.size)
                positions = [(row, col + i) for i in range(vessel.size)]

            if all((r, c) not in occupied for r, c in positions):
                for r, c in positions:
                    occupied.add((r, c))
                BoardVessel.objects.create(
                    board=board,
                    vessel=vessel,
                    ri=positions[0][0],
                    ci=positions[0][1],
                    rf=positions[-1][0],
                    cf=positions[-1][1],
                )
                placed = True

    board.prepared = True
    board.save()

from .models import Player, Game, Board, Vessel, BoardVessel, Shot
from .serializers import (
    UserSerializer,
    PlayerSerializer,
    GameSerializer,
    BoardSerializer,
    VesselSerializer,
    BoardVesselSerializer,
    ShotSerializer,
    PlayerStateSerializer,
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']
    permission_classes = [permissions.AllowAny]


class PlayerViewSet(viewsets.ModelViewSet):
    """
    Provides list, create, retrieve, update, destroy for Player.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nickname']
    permission_classes = [permissions.AllowAny]


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='players/(?P<player_id>[^/.]+)/vessels')
    def add_vessel(self, request, pk=None, player_id=None):
        game = self.get_object()
        player = get_object_or_404(Player, pk=player_id)

        # Aquí obtén el board del jugador en ese juego
        board = Board.objects.filter(game=game, player=player).first()
        if not board:
            return Response({"detail": "Board not found."}, status=404)

        vessel_data = request.data.get("vessel", {})
        vessel = get_object_or_404(Vessel, pk=vessel_data.get("type"))

        board_vessel = BoardVessel.objects.create(
            board=board,
            vessel=vessel,
            ri=vessel_data["x"],
            ci=vessel_data["y"],
            rf=vessel_data["x"] + (vessel.size - 1 if vessel_data["isVertical"] else 0),
            cf=vessel_data["y"] + (0 if vessel_data["isVertical"] else vessel.size - 1),
        )

        available = PlayerStateSerializer(board).get_availableShips(board)

        if not available:
            board.prepared = True
            board.save()

            # Forzar al bot a colocar sus barcos
            bot_board = Board.objects.filter(game=game).exclude(player=player).first()
            if bot_board and not bot_board.prepared:
                place_bot_ships(bot_board)

            # Comprobar si ambos están listos y actualizar juego
            boards = Board.objects.filter(game=game)
            if all(b.prepared for b in boards) and game.phase != "playing":
                game.phase = "playing"
                game.turn = game.owner
                game.save()

        return Response(BoardVesselSerializer(board_vessel).data, status=201)

    @action(detail=True, methods=["post"], url_path="players/(?P<player_id>[^/.]+)/shots")
    def add_shot(self, request, pk=None, player_id=None):
        import random

        game = self.get_object()
        player = get_object_or_404(Player, pk=player_id)

        if game.phase != "playing":
            boards = Board.objects.filter(game=game)
            if all(b.prepared for b in boards):
                game.phase = "playing"
                if game.turn is None:
                    game.turn = player
                game.save()

        opponent_board = Board.objects.filter(game=game).exclude(player=player).first()
        if not opponent_board:
            return Response({"detail": "Board not found"}, status=404)

        shot_data = request.data.get("shotData", {})
        row = shot_data.get("x")
        col = shot_data.get("y")

        if Shot.objects.filter(board=opponent_board, row=row, col=col).exists():
            return Response({"detail": "Already shot here"}, status=400)

        result = 10
        for vessel in BoardVessel.objects.filter(board=opponent_board):
            rows = range(min(vessel.ri, vessel.rf), max(vessel.ri, vessel.rf) + 1)
            cols = range(min(vessel.ci, vessel.cf), max(vessel.ci, vessel.cf) + 1)
            if row in rows and col in cols:
                result = -vessel.vessel.id
                impact_positions = {(r, c) for r in rows for c in cols}
                shots = Shot.objects.filter(board=opponent_board, row__in=rows, col__in=cols)
                shot_positions = {(s.row, s.col) for s in shots}.union({(row, col)})
                if impact_positions.issubset(shot_positions):
                    vessel.alive = False
                    vessel.save()
                break

        Shot.objects.create(
            game=game,
            board=opponent_board,
            player=player,
            row=row,
            col=col,
            result=result,
        )

        if not BoardVessel.objects.filter(board=opponent_board, alive=True).exists():
            game.winner = player
            game.phase = "gameOver"
            game.save()
            serializer = self.get_serializer(game, context={"request": request})
            return Response(serializer.data, status=201)

        if not game.multiplayer:
            player_board = Board.objects.get(game=game, player=player)
            available_targets = [
                (r, c)
                for r in range(game.width)
                for c in range(game.height)
                if not Shot.objects.filter(board=player_board, row=r, col=c).exists()
            ]
            if available_targets:
                r, c = random.choice(available_targets)
                bot_result = 10
                for vessel in BoardVessel.objects.filter(board=player_board):
                    rows = range(min(vessel.ri, vessel.rf), max(vessel.ri, vessel.rf) + 1)
                    cols = range(min(vessel.ci, vessel.cf), max(vessel.ci, vessel.cf) + 1)
                    if r in rows and c in cols:
                        bot_result = -vessel.vessel.id
                        impact_positions = {(i, j) for i in rows for j in cols}
                        shots = Shot.objects.filter(board=player_board, row__in=rows, col__in=cols)
                        shot_positions = {(s.row, s.col) for s in shots}.union({(r, c)})
                        if impact_positions.issubset(shot_positions):
                            vessel.alive = False
                            vessel.save()
                        break

                bot_player = opponent_board.player
                Shot.objects.create(
                    game=game,
                    board=player_board,
                    player=bot_player,
                    row=r,
                    col=c,
                    result=bot_result,
                )

                if not BoardVessel.objects.filter(board=player_board, alive=True).exists():
                    game.winner = bot_player
                    game.phase = "gameOver"
                    game.save()
                    serializer = self.get_serializer(game, context={"request": request})
                    return Response(serializer.data, status=201)

            game.turn = player
            game.save()

        serializer = self.get_serializer(game, context={"request": request})
        return Response(serializer.data, status=201)

    def create(self, request, *args, **kwargs):
        seed_vessels()

        player_id = request.data.get("playerId")
        multiplayer = request.data.get("multiplayer", False)

        # Obtener el jugador real
        player = get_object_or_404(Player, id=player_id)

        # Crear el juego y asociar al jugador humano
        game = Game.objects.create(multiplayer=multiplayer, owner=player)
        game.players.add(player)
        Board.objects.create(game=game, player=player)

        # 🔧 Añadir automáticamente el jugador bot
        bot_user, created = User.objects.get_or_create(username="bot")
        if created:
            bot_user.set_password("botpass")  # opcional, no necesario
            bot_user.save()

        bot_player, _ = Player.objects.get_or_create(user=bot_user, defaults={"nickname": "Bot"})
        game.players.add(bot_player)
        Board.objects.create(game=game, player=bot_player)

        game.phase = "placement"
        game.save()

        # Serializar el juego con contexto (para el game_state_response)
        serializer = self.get_serializer(game, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BoardViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD for Board.
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class VesselViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD for Vessel.
    """
    queryset = Vessel.objects.all()
    serializer_class = VesselSerializer


class BoardVesselViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD for BoardVessel (placement of vessels on boards).
    """
    queryset = BoardVessel.objects.all()
    serializer_class = BoardVesselSerializer


class ShotViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD for Shot (player shots on boards)...
    """
    queryset = Shot.objects.all()
    serializer_class = ShotSerializer