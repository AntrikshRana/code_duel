from django.urls import path
from .views import (
    CreateBattleView,
    JoinBattleView,
    BattleDetailView,
    ActiveBattlesListView,
    JoinMatchmakingView,
    CheckMatchmakingStatusView,
    LeaveMatchmakingView
)

urlpatterns = [
    path('create/', CreateBattleView.as_view(), name='battle_create'),
    path('join/', JoinBattleView.as_view(), name='battle_join'),
    path('active/', ActiveBattlesListView.as_view(), name='battle_active_list'),
    path('matchmaking/join/', JoinMatchmakingView.as_view(), name='matchmaking_join'),
    path('matchmaking/status/', CheckMatchmakingStatusView.as_view(), name='matchmaking_status'),
    path('matchmaking/leave/', LeaveMatchmakingView.as_view(), name='matchmaking_leave'),
    path('<str:room_code>/', BattleDetailView.as_view(), name='battle_detail'),
]
