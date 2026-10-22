import random
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Battle
from .serializers import BattleSerializer
from problems.models import Problem

class CreateBattleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        problem_id = request.data.get('problem_id')
        if problem_id:
            problem = get_object_or_404(Problem, id=problem_id)
        else:
            # Pick a random problem
            problems = list(Problem.objects.all())
            if not problems:
                return Response({"error": "No problems available in database."}, status=status.HTTP_400_BAD_REQUEST)
            problem = random.choice(problems)

        battle = Battle.objects.create(
            problem=problem,
            player1=request.user,
            status='WAITING'
        )
        return Response(BattleSerializer(battle).data, status=status.HTTP_201_CREATED)

class JoinBattleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        room_code = request.data.get('room_code', '').strip().upper()
        battle = get_object_or_404(Battle, room_code=room_code)

        if battle.player1 == request.user:
            return Response(BattleSerializer(battle).data, status=status.HTTP_200_OK)

        if battle.player2 and battle.player2 != request.user:
            return Response({"error": "Room is already full."}, status=status.HTTP_400_BAD_REQUEST)

        if not battle.player2:
            battle.player2 = request.user
            battle.status = 'COUNTDOWN'
            battle.start_time = timezone.now()
            battle.save()

        return Response(BattleSerializer(battle).data, status=status.HTTP_200_OK)

class BattleDetailView(generics.RetrieveAPIView):
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'room_code'

class ActiveBattlesListView(generics.ListAPIView):
    serializer_class = BattleSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Battle.objects.filter(status__in=['WAITING', 'IN_PROGRESS', 'COUNTDOWN']).order_by('-created_at')[:20]
