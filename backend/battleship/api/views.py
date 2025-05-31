from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, OpenApiParameter



from .models import Player, Game, Board, Vessel, BoardVessel, Shot
from .serializers import (
    UserSerializer,
    PlayerSerializer,
    GameSerializer,
    BoardSerializer,
    VesselSerializer,
    BoardVesselSerializer,
    ShotSerializer,
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

        return Response(BoardVesselSerializer(board_vessel).data, status=201)

    def create(self, request, *args, **kwargs):
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