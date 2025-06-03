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

    def get_winner(self, obj):
        if obj.winner:
            return obj.winner.nickname
        return None

    def get_player1(self, obj):
        player = obj.players.exclude(user__username="bot").first()
        board = Board.objects.filter(game=obj, player=player).first()
        return PlayerStateSerializer(board).data if board else None

    def get_player2(self, obj):
        player = obj.players.filter(user__username="bot").first()
        board = Board.objects.filter(game=obj, player=player).first()
        return PlayerStateSerializer(board).data if board else None

class PlayerStateSerializer(serializers.Serializer):
    id = serializers.CharField(source='player.id')
    username = serializers.CharField(source='player.nickname')
    placedShips = serializers.SerializerMethodField()
    availableShips = serializers.SerializerMethodField()
    board = serializers.SerializerMethodField()

    def get_placedShips(self, board):
        ships = []
        for board_vessel in BoardVessel.objects.filter(board=board):
            ships.append({
                'type': board_vessel.vessel.id,
                'position': {
                    'row': board_vessel.ri,
                    'col': board_vessel.ci
                },
                'isVertical': board_vessel.rf != board_vessel.ri,
                'size': board_vessel.vessel.size
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

        shot_map = {(s.row, s.col): s.result for s in Shot.objects.filter(board=board)}

        for vessel in BoardVessel.objects.filter(board=board):
            for i in range(min(vessel.ri, vessel.rf), max(vessel.ri, vessel.rf) + 1):
                for j in range(min(vessel.ci, vessel.cf), max(vessel.ci, vessel.cf) + 1):
                    if (i, j) in shot_map:
                        grid[i][j] = -vessel.vessel.id
                    else:
                        grid[i][j] = vessel.vessel.id

        for (i, j), result in shot_map.items():
            if grid[i][j] == 0:
                grid[i][j] = 11  # Agua

        return grid

    def get_availableShips(self, board):
        game = board.game
        player = board.player

        all_vessels = Vessel.objects.all()

        placed_vessels = BoardVessel.objects.filter(board=board).values_list('vessel_id', flat=True)

        available_vessels = []
        for vessel in all_vessels:
            if vessel.id not in placed_vessels:
                available_vessels.append({
                    "type": vessel.id,
                    "size": vessel.size,
                    "isVertical": True
                })

        return available_vessels
