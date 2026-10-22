from django.urls import path
from .views import CreateBattleView, JoinBattleView, BattleDetailView, ActiveBattlesListView

urlpatterns = [
    path('create/', CreateBattleView.as_view(), name='battle_create'),
    path('join/', JoinBattleView.as_view(), name='battle_join'),
    path('active/', ActiveBattlesListView.as_view(), name='battle_active_list'),
    path('<str:room_code>/', BattleDetailView.as_view(), name='battle_detail'),
]
