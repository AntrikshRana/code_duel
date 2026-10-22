from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer
from .models import UserProfile
from battles.models import Battle, MatchmakingQueue

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class LeaderboardView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        profiles = UserProfile.objects.select_related('user').order_by('-rating')[:50]
        data = [
            {
                "username": p.user.username,
                "rating": p.rating,
                "wins": p.wins,
                "losses": p.losses,
                "draws": p.draws,
                "avatar_url": p.avatar_url,
                "win_rate": round((p.wins / (p.wins + p.losses) * 100), 1) if (p.wins + p.losses) > 0 else 0
            }
            for p in profiles
        ]
        return Response(data)

class OnlineStatsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        now = timezone.now()
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            request.user.profile.save()

        five_mins_ago = now - timedelta(minutes=5)
        online_count = UserProfile.objects.filter(updated_at__gte=five_mins_ago).count()
        if online_count == 0 and request.user.is_authenticated:
            online_count = 1

        active_battles_count = Battle.objects.filter(status__in=['COUNTDOWN', 'IN_PROGRESS']).count()
        in_queue_count = MatchmakingQueue.objects.filter(matched_room_code__isnull=True).count()
        total_registered = User.objects.count()

        return Response({
            "online_users": max(1, online_count),
            "in_battles": active_battles_count * 2,
            "in_queue": in_queue_count,
            "total_registered": total_registered
        })
