from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, QuickGuestView, CurrentUserView, LeaderboardView, OnlineStatsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('guest/', QuickGuestView.as_view(), name='guest_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', CurrentUserView.as_view(), name='current_user'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('online-stats/', OnlineStatsView.as_view(), name='online_stats'),
]

