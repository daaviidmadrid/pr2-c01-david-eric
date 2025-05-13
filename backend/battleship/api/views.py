from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .models import Player, Game
from .serializers import UserSerializer, PlayerSerializer, GameSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides list and retrieve actions for Django User model.
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
        # Assign the owner of the game to the first User's Player (placeholder logic)
        player = get_object_or_404(Player, user=User.objects.first())
        serializer.save(owner=player)