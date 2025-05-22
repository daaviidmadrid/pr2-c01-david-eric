from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .serializers import PlayerSerializer, GameSerializer, UserSerializer
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


class PlayerViewSet(viewsets.ModelViewSet):
    """
    Provides list, create, retrieve, update, destroy for Player.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nickname']


class GameViewSet(viewsets.ModelViewSet):
    """
    Provides list, create, retrieve, update, destroy for Game.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['phase']
    ordering_fields = ['id']

    def perform_create(self, serializer):
        # Placeholder: assign owner as first User's Player
        player = get_object_or_404(Player, user=User.objects.first())
        serializer.save(owner=player)

    @action(detail=True, methods=['get'], url_path='players/(?P<pid>[^/.]+)')
    def retrieve_player(self, request, pk=None, pid=None):
        game = self.get_object()
        player = get_object_or_404(Player, pk=pid)

        if player not in game.players.all():
            return Response({'detail': 'Player not in this game.'}, status=404)

        serializer = PlayerSerializer(player)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], url_path='players/(?P<pid>[^/.]+)')
    def remove_player(self, request, pk=None, pid=None):
        game = get_object_or_404(Game, pk=pk)
        player = get_object_or_404(Player, pk=pid)

        if player in game.players.all():
            game.players.remove(player)
            return Response(status=204)
        return Response({'detail': 'Player not in this game.'}, status=404)

    @action(detail=True, methods=['get', 'post'], url_path='players/(?P<pid>[^/.]+)/vessels')
    def player_vessels(self, request, pk=None, pid=None):
        game = self.get_object()
        player = get_object_or_404(Player, id=pid)
        board = get_object_or_404(Board, game=game, player=player)

        if request.method == 'GET':
            vessels = BoardVessel.objects.filter(board=board)
            serializer = BoardVesselSerializer(vessels, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            data = request.data.copy()
            data['board'] = board.id
            serializer = BoardVesselSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get', 'put', 'patch', 'delete'],
            url_path='players/(?P<pid>[^/.]+)/vessels/(?P<vid>[^/.]+)')
    def player_vessel_detail(self, request, pk=None, pid=None, vid=None):
        game = self.get_object()
        player = get_object_or_404(Player, id=pid)
        board = get_object_or_404(Board, game=game, player=player)
        vessel = get_object_or_404(BoardVessel, id=vid, board=board)

        if request.method == 'GET':
            serializer = BoardVesselSerializer(vessel)
            return Response(serializer.data)
        elif request.method in ['PUT', 'PATCH']:
            serializer = BoardVesselSerializer(vessel, data=request.data, partial=(request.method == 'PATCH'))
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            vessel.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get', 'post'], url_path='players/(?P<pid>[^/.]+)/shots')
    def player_shots(self, request, pk=None, pid=None):
        game = self.get_object()
        player = get_object_or_404(Player, id=pid)
        if request.method == 'GET':
            shots = Shot.objects.filter(game=game, player=player)
            serializer = ShotSerializer(shots, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            data = request.data.copy()
            data['game'] = game.id
            data['player'] = player.id
            serializer = ShotSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='players/(?P<pid>[^/.]+)/shots/(?P<sid>[^/.]+)')
    def player_shot_detail(self, request, pk=None, pid=None, sid=None):
        game = self.get_object()
        player = get_object_or_404(Player, id=pid)
        shot = get_object_or_404(Shot, id=sid, game=game, player=player)
        serializer = ShotSerializer(shot)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='players/(?P<pid>[^/.]+)/boards')
    def player_boards(self, request, pk=None, pid=None):
        game = self.get_object()
        player = get_object_or_404(Player, id=pid)
        boards = Board.objects.filter(game=game, player=player)
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='players/(?P<pid>[^/.]+)/boards/(?P<bid>[^/.]+)')
    def player_board_detail(self, request, pk=None, pid=None, bid=None):
        game = self.get_object()
        player = get_object_or_404(Player, id=pid)
        board = get_object_or_404(Board, id=bid, game=game, player=player)
        serializer = BoardSerializer(board)
        return Response(serializer.data)


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