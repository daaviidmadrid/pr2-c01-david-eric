from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

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

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides list and retrieve for Django User model.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


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