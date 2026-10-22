import random
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Battle, MatchmakingQueue
from .serializers import BattleSerializer
from problems.models import Problem

class CreateBattleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        problem_id = request.data.get('problem_id')
        if problem_id:
            problem = get_object_or_404(Problem, id=problem_id)
        else:
            problems = list(Problem.objects.all())
            if not problems:
                return Response({"error": "No problems available in database."}, status=status.HTTP_400_BAD_REQUEST)
            problem = random.choice(problems)

        battle = Battle.objects.create(
            problem=problem,
            player1=request.user,
            status='WAITING',
            is_ranked=False
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

# ==========================================
# AUTOMATED ELO MATCHMAKING SYSTEM
# ==========================================
class JoinMatchmakingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        my_rating = getattr(request.user.profile, 'rating', 0)
        diff_pref = request.data.get('difficulty', 'ANY').upper()

        # Clean any stale entry for current user
        MatchmakingQueue.objects.filter(user=request.user).delete()

        # Search for available opponent currently in queue
        queue_candidates = MatchmakingQueue.objects.filter(
            matched_room_code__isnull=True
        ).exclude(user=request.user)

        # Filter by difficulty preference if specific tier requested
        if diff_pref in ['EASY', 'MEDIUM', 'HARD']:
            queue_candidates = queue_candidates.filter(
                difficulty_preference__in=[diff_pref, 'ANY']
            )

        opponent_ticket = None
        candidates_list = list(queue_candidates.order_by('created_at'))
        if candidates_list:
            # Sort by closest rating to current player
            candidates_list.sort(key=lambda c: abs(c.rating - my_rating))
            opponent_ticket = candidates_list[0]

        if opponent_ticket:
            # Match found! Pick problem matching requested difficulty
            target_diff = diff_pref if diff_pref in ['EASY', 'MEDIUM', 'HARD'] else opponent_ticket.difficulty_preference
            problems = Problem.objects.all()
            if target_diff in ['EASY', 'MEDIUM', 'HARD']:
                matched_probs = list(problems.filter(difficulty=target_diff))
                problem = random.choice(matched_probs) if matched_probs else random.choice(list(problems))
            else:
                problem = random.choice(list(problems))

            battle = Battle.objects.create(
                problem=problem,
                player1=opponent_ticket.user,
                player2=request.user,
                status='COUNTDOWN',
                start_time=timezone.now(),
                is_ranked=True
            )

            # Signal opponent ticket
            opponent_ticket.matched_room_code = battle.room_code
            opponent_ticket.save()

            return Response({
                "matched": True,
                "room_code": battle.room_code,
                "opponent": opponent_ticket.user.username,
                "problem_title": problem.title
            }, status=status.HTTP_200_OK)

        # No opponent yet: put user in queue
        ticket = MatchmakingQueue.objects.create(
            user=request.user,
            rating=my_rating,
            difficulty_preference=diff_pref
        )

        return Response({
            "matched": False,
            "message": "Searching for an opponent...",
            "my_rating": my_rating
        }, status=status.HTTP_200_OK)

class CheckMatchmakingStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        ticket = MatchmakingQueue.objects.filter(user=request.user).first()
        if not ticket:
            return Response({"matched": False, "queued": False})

        if ticket.matched_room_code:
            room_code = ticket.matched_room_code
            ticket.delete()
            return Response({
                "matched": True,
                "room_code": room_code
            })

        return Response({
            "matched": False,
            "queued": True,
            "rating": ticket.rating
        })

class LeaveMatchmakingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        MatchmakingQueue.objects.filter(user=request.user).delete()
        return Response({"message": "Left matchmaking queue."}, status=status.HTTP_200_OK)
