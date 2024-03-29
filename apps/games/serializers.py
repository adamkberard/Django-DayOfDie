from rest_framework import serializers

from apps.core.validators import validate_players
from apps.players.models import Player
from apps.players.serializers import PlayerReadSerializer
from apps.teams.models import Team
from apps.teams.serializers import TeamSerializer

from .models import Game, Point


class PointWriteSerializer(serializers.Serializer):
    scorer = serializers.UUIDField()
    type = serializers.ChoiceField(choices=[x[0] for x in Point.TYPE_CHOICES])


class GameWriteSerializer(serializers.Serializer):
    playerOne = serializers.UUIDField(validators=[validate_players])
    playerTwo = serializers.UUIDField(validators=[validate_players])
    playerThree = serializers.UUIDField(validators=[validate_players])
    playerFour = serializers.UUIDField(validators=[validate_players])

    home_team_score = serializers.IntegerField()
    away_team_score = serializers.IntegerField()

    time_started = serializers.DateTimeField()
    time_ended = serializers.DateTimeField()

    points = PointWriteSerializer(many=True)

    def to_representation(self, instance):
        rep = GameSerializer(instance).data
        return rep

    def create(self, validated_data):
        points_data = validated_data.pop('points')

        # Must find the teams myself, if they don't exist I create them
        playerOne = Player.objects.get(uuid=validated_data.pop('playerOne'), is_staff=False)
        playerTwo = Player.objects.get(uuid=validated_data.pop('playerTwo'), is_staff=False)
        playerThree = Player.objects.get(uuid=validated_data.pop('playerThree'), is_staff=False)
        playerFour = Player.objects.get(uuid=validated_data.pop('playerFour'), is_staff=False)

        _, home_team = Team.objects.get_or_create_team(playerOne, playerTwo)
        _, away_team = Team.objects.get_or_create_team(playerThree, playerFour)

        home_team.save()
        away_team.save()

        # Created games are always unconfirmed
        game = Game.objects.create(**validated_data, home_team=home_team,
                                   away_team=away_team, confirmed=False)

        for point_data in points_data:
            scorer = Player.objects.get(uuid=point_data.get('scorer'), is_staff=False)
            type = point_data.get('type')
            Point.objects.create(game=game, scorer=scorer, type=type)

        return game


class PointSerializer(serializers.ModelSerializer):
    scorer = PlayerReadSerializer()

    class Meta:
        model = Point
        exclude = ['created', 'modified', 'game']


class GameSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True)
    home_team = TeamSerializer()
    away_team = TeamSerializer()

    class Meta:
        model = Game
        exclude = ['created', 'modified']

    def to_representation(self, instance):
        instance.points = []
        representation = super().to_representation(instance)
        points_set = Point.objects.filter(game=instance)
        serialized_points = PointSerializer(points_set, many=True)
        representation['points'] = serialized_points.data

        representation['time_started'] = instance.time_started.isoformat()
        representation['time_ended'] = instance.time_ended.isoformat()

        return representation
