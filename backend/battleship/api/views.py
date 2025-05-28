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