from rest_framework import serializers
from .models import Battle, BattleEvent
from problems.serializers import ProblemDetailSerializer
from problems.models import Problem

class BattleSerializer(serializers.ModelSerializer):
    player1_name = serializers.CharField(source='player1.username', read_only=True)
    player2_name = serializers.CharField(source='player2.username', read_only=True, allow_null=True)
    player1_rating = serializers.IntegerField(source='player1.profile.rating', read_only=True)
    player2_rating = serializers.IntegerField(source='player2.profile.rating', read_only=True, allow_null=True)
    winner_name = serializers.CharField(source='winner.username', read_only=True, allow_null=True)
    problem_details = ProblemDetailSerializer(source='problem', read_only=True)

    class Meta:
        model = Battle
        fields = [
            'id', 'room_code', 'problem', 'problem_details',
            'player1', 'player1_name', 'player1_rating', 'player1_ready', 'player1_solved_at',
            'player2', 'player2_name', 'player2_rating', 'player2_ready', 'player2_solved_at',
            'status', 'winner', 'winner_name', 'start_time', 'end_time',
            'thinking_seconds', 'coding_seconds', 'duration_seconds',
            'winner_points_gained', 'complexity_bonus',
            'created_at'
        ]
        read_only_fields = ['room_code', 'player1', 'status', 'winner', 'player1_solved_at', 'player2_solved_at', 'start_time', 'end_time', 'winner_points_gained', 'complexity_bonus']
