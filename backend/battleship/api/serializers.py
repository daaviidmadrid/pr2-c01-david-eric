from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Player, Game, Board, Vessel, BoardVessel, Shot

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '_all_'

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '_all_'

class GameSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.user.username')

    class Meta:
        model = Game
        fields = '_all_'

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '_all_'

class VesselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vessel
        fields = '_all_'

class BoardVesselSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardVessel
        fields = '_all_'

class ShotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shot
        fields = '_all_'