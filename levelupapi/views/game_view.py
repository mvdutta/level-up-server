"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType


class GameView(ViewSet):
    """Level up game types view"""

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single ticket
            Returns:
            Response -- JSON serialized ticket record
        """

        game = Game.objects.get(pk=pk)
        serialized = GameSerializer(
            game, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        game_type = GameType.objects.get(pk=request.data["game_type"])

        game = Game.objects.create(
            game_title=request.data["game_title"],
            maker=request.data["maker"],
            num_of_players=request.data["num_of_players"],
            skill_level=request.data["skill_level"],
            creator=gamer,
            type=game_type
        )
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreatorSerializer(serializers.ModelSerializer):
    """JSON serializer for creator on games"""
    class Meta:
        model = Gamer
        fields = ('id', 'bio', 'full_name',)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    creator = CreatorSerializer(many=False)
    class Meta:
        model = Game
        fields = ('id', 'game_title', 'type', 'creator', 'skill_level', 'maker', 'num_of_players')
        depth = 1