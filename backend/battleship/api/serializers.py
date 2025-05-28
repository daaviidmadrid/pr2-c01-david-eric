from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Player, Game, Board, Vessel, BoardVessel, Shot

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Les contrasenyes no coincideixen.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # eliminem el segon camp de contrasenya
        user = User.objects.create_user(**validated_data)  # crea amb hashing
        return user

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    game_state_response = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ['id', 'phase', 'turn', 'winner', 'game_state_response']

    def get_game_state_response(self, obj):
        return GameStateResponseSerializer(obj, context=self.context).data

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

class VesselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vessel
        fields = '__all__'

class BoardVesselSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardVessel
        fields = '__all__'

class ShotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shot
        fields = '__all__'

class GameStateResponseSerializer(serializers.Serializer):
    # status = serializers.IntegerField(default=200)
    # message = serializers.CharField(default="OK")
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        return {
            'gameState': GameStateSerializer(obj).data
        }

class GameStateSerializer(serializers.Serializer):
    gameId = serializers.CharField(source='id')
    phase = serializers.CharField()
    turn = serializers.CharField(source='turn.nickname', allow_null=True)
    winner = serializers.CharField(source='winner.nickname', allow_null=True)
    player1 = serializers.SerializerMethodField()
    player2 = serializers.SerializerMethodField()

    def get_player1(self, obj):
        request = self.context.get('request')
        if not request:
            return None
        current_player = request.user.player
        board = Board.objects.get(game=obj, owner=current_player)
        return PlayerStateSerializer(board).data

    def get_player2(self, obj):
        request = self.context.get('request')
        if not request:
            return None
        current_player = request.user.player
        board = obj.board_set.exclude(owner=current_player).first()
        return PlayerStateSerializer(board).data if board else None

class PlayerStateSerializer(serializers.Serializer):
    id = serializers.CharField(source='owner.id')
    username = serializers.CharField(source='owner.nickname')
    placedShips = serializers.SerializerMethodField()
    availableShips = serializers.SerializerMethodField()
    board = serializers.SerializerMethodField()

    def get_placedShips(self, board):
        ships = []
        for vessel in BoardVessel.objects.filter(board=board):
            ships.append({
                'type': vessel.type.id,
                'position': {
                    'row': vessel.ri,
                    'col': vessel.ci
                },
                'isVertical': vessel.rf != vessel.ri,
                'size': vessel.type.size
            })
        return ships

    def get_availableShips(self, board):
        all_vessels = Vessel.objects.all()
        placed_vessels = BoardVessel.objects.filter(board=board)
        ships = []

        for vessel in all_vessels:
            if not placed_vessels.filter(type=vessel).exists():
                ships.append({
                    'type': vessel.id,
                    'isVertical': True,
                    'size': vessel.size
                })
        return ships

    def get_board(self, board):
        size = board.game.width
        grid = [[0 for _ in range(size)] for _ in range(size)]

        for vessel in BoardVessel.objects.filter(board=board):
            value = vessel.type.id if vessel.alive else -vessel.type.id
            for i in range(min(vessel.ri, vessel.rf), max(vessel.ri, vessel.rf) + 1):
                for j in range(min(vessel.ci, vessel.cf), max(vessel.ci, vessel.cf) + 1):
                    grid[i][j] = value

        for shot in Shot.objects.filter(board=board):
            if grid[shot.row][shot.col] == 0:
                grid[shot.row][shot.col] = 11

        return grid