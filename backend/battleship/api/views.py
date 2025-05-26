# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Player, Game, Board, Vessel, BoardVessel, Shot
from .serializers import (
    UserSerializer, PlayerSerializer, GameSerializer,
    BoardSerializer, VesselSerializer, BoardVesselSerializer, ShotSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    """
    GET    /user/
    POST   /user/
    GET    /user/{id}/
    PUT    /user/{id}/
    PATCH  /user/{id}/
    DELETE /user/{id}/
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PlayerViewSet(viewsets.ModelViewSet):
    """
    GET    /players/
    POST   /players/
    GET    /players/{id}/
    PUT    /players/{id}/
    PATCH  /players/{id}/
    DELETE /players/{id}/
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

class GameViewSet(viewsets.ModelViewSet):
    """
    GET    /games/
    POST   /games/
    GET    /games/{gid}/
    PUT    /games/{gid}/
    PATCH  /games/{gid}/
    DELETE /games/{gid}/

    GET    /games/{gid}/players/
    POST   /games/{gid}/players/
    GET    /games/{gid}/players/{pid}/
    DELETE /games/{gid}/players/{pid}/

    GET    /games/{gid}/players/{pid}/boards/
    GET    /games/{gid}/players/{pid}/boards/{bid}/

    GET    /games/{gid}/players/{pid}/vessels/
    POST   /games/{gid}/players/{pid}/vessels/
    GET    /games/{gid}/players/{pid}/vessels/{vid}/
    PUT    /games/{gid}/players/{pid}/vessels/{vid}/
    PATCH  /games/{gid}/players/{pid}/vessels/{vid}/
    DELETE /games/{gid}/players/{pid}/vessels/{vid}/

    GET    /games/{gid}/players/{pid}/shots/
    POST   /games/{gid}/players/{pid}/shots/
    GET    /games/{gid}/players/{pid}/shots/{sid}/
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def perform_create(self, serializer):
        player = get_object_or_404(Player, user=User.objects.first())
        serializer.save(owner=player)

    # Players nested
    @action(detail=True, methods=['get', 'post'], url_path='players')
    def players_list(self, request, gid=None):
        game = self.get_object()
        if request.method == 'GET':
            players = game.players.all()
            serializer = PlayerSerializer(players, many=True)
            return Response(serializer.data)
        pid = request.data.get('id')
        player = get_object_or_404(Player, pk=pid)
        game.players.add(player)
        return Response(PlayerSerializer(player).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'delete'], url_path=r'players/(?P<pid>[^/.]+)')
    def player_detail(self, request, gid=None, pid=None):
        game = self.get_object()
        player = get_object_or_404(Player, pk=pid)
        if request.method == 'GET':
            return Response(PlayerSerializer(player).data)
        game.players.remove(player)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Boards nested
    @action(detail=True, methods=['get'], url_path=r'players/(?P<pid>[^/.]+)/boards')
    def player_boards(self, request, gid=None, pid=None):
        game = self.get_object()
        player = get_object_or_404(Player, pk=pid)
        boards = Board.objects.filter(game=game, player=player)
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path=r'players/(?P<pid>[^/.]+)/boards/(?P<bid>[^/.]+)')
    def player_board(self, request, gid=None, pid=None, bid=None):
        game = self.get_object()
        player = get_object_or_404(Player, pk=pid)
        board = get_object_or_404(Board, pk=bid, game=game, player=player)
        return Response(BoardSerializer(board).data)

    # Vessels nested
    @action(detail=True, methods=['get', 'post'], url_path=r'players/(?P<pid>[^/.]+)/vessels')
    def player_vessels(self, request, gid=None, pid=None):
        game = self.get_object()
        player = get_object_or_404(Player, pk=pid)
        if request.method == 'GET':
            bv_qs = BoardVessel.objects.filter(board__game=game, board__player=player)
            return Response(BoardVesselSerializer(bv_qs, many=True).data)
        serializer = BoardVesselSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        board = get_object_or_404(
            Board, pk=request.data.get('board'), game=game, player=player
        )
        serializer.save(board=board)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'put', 'patch', 'delete'], url_path=r'players/(?P<pid>[^/.]+)/vessels/(?P<vid>[^/.]+)')
    def player_vessel_detail(self, request, gid=None, pid=None, vid=None):
        game = self.get_object()
        player = get_object_or_404(Player, pk=pid)
        bv = get_object_or_404(
            BoardVessel, pk=vid, board__game=game, board__player=player
        )
        if request.method == 'GET':
            return Response(BoardVesselSerializer(bv).data)
        if request.method in ['PUT', 'PATCH']:
            partial = request.method == 'PATCH'
            serializer = BoardVesselSerializer(bv, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        bv.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Shots nested
    @action(detail=True, methods=['get', 'post'], url_path=r'players/(?P<pid>[^/.]+)/shots')
    def player_shots(self, request, gid=None, pid=None):
        game = self.get_object()
        player = get_object_or_404(Player, pk=pid)
        if request.method == 'GET':
            shots = Shot.objects.filter(game=game, player=player)
            return Response(ShotSerializer(shots, many=True).data)
        serializer = ShotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        board = get_object_or_404(
            Board, pk=request.data.get('board'), game=game, player=player
        )
        serializer.save(game=game, player=player, board=board)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path=r'players/(?P<pid>[^/.]+)/shots/(?P<sid>[^/.]+)')
    def player_shot(self, request, gid=None, pid=None, sid=None):
        game = self.get_object()
        player = get_object_or_404(Player, pk=pid)
        shot = get_object_or_404(
            Shot, pk=sid, game=game, player=player
        )
        return Response(ShotSerializer(shot).data)


class BoardViewSet(viewsets.ModelViewSet):
    """
    GET    /boards/
    POST   /boards/
    GET    /boards/{id}/
    PUT    /boards/{id}/
    PATCH  /boards/{id}/
    DELETE /boards/{id}/
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class VesselViewSet(viewsets.ModelViewSet):
    """
    GET    /vessels/
    POST   /vessels/
    GET    /vessels/{id}/
    PUT    /vessels/{id}/
    PATCH  /vessels/{id}/
    DELETE /vessels/{id}/
    """
    queryset = Vessel.objects.all()
    serializer_class = VesselSerializer

class BoardVesselViewSet(viewsets.ModelViewSet):
    """
    GET    /boardvessels/
    POST   /boardvessels/
    GET    /boardvessels/{id}/
    PUT    /boardvessels/{id}/
    PATCH  /boardvessels/{id}/
    DELETE /boardvessels/{id}/
    """
    queryset = BoardVessel.objects.all()
    serializer_class = BoardVesselSerializer

class ShotViewSet(viewsets.ModelViewSet):
    """
    GET    /shots/
    POST   /shots/
    GET    /shots/{id}/
    PUT    /shots/{id}/
    PATCH  /shots/{id}/
    DELETE /shots/{id}/
    """
    queryset = Shot.objects.all()
    serializer_class = ShotSerializer

