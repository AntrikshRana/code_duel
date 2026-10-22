import random
import string
from django.db import models
from django.contrib.auth.models import User
from problems.models import Problem

def generate_room_code():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=6))

class Battle(models.Model):
    STATUS_CHOICES = [
        ('WAITING', 'Waiting for Opponent'),
        ('COUNTDOWN', 'Starting Countdown'),
        ('IN_PROGRESS', 'Battle In Progress'),
        ('COMPLETED', 'Battle Finished'),
        ('DRAW', 'Match Tied / Time Expired'),
        ('CANCELLED', 'Cancelled'),
    ]

    room_code = models.CharField(max_length=10, unique=True, default=generate_room_code)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='battles')
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='battles_as_p1')
    player2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='battles_as_p2')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='WAITING')
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='battles_won')
    
    player1_ready = models.BooleanField(default=False)
    player2_ready = models.BooleanField(default=False)
    
    player1_solved_at = models.DateTimeField(null=True, blank=True)
    player2_solved_at = models.DateTimeField(null=True, blank=True)
    
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    # 5 min Thinking Phase (300s) + Coding Phase (Easy: 15m, Med: 25m, Hard: 35m)
    thinking_seconds = models.PositiveIntegerField(default=300)
    coding_seconds = models.PositiveIntegerField(default=900)
    duration_seconds = models.PositiveIntegerField(default=1200)

    # Points earned breakdown
    winner_points_gained = models.IntegerField(default=0)
    complexity_bonus = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.problem:
            self.thinking_seconds = 300 # 5 minutes thinking time
            diff = self.problem.difficulty.upper()
            if diff == 'EASY':
                self.coding_seconds = 15 * 60 # 15 minutes (900s)
            elif diff == 'MEDIUM':
                self.coding_seconds = 25 * 60 # 25 minutes (1500s)
            elif diff == 'HARD':
                self.coding_seconds = 35 * 60 # 35 minutes (2100s)
            self.duration_seconds = self.thinking_seconds + self.coding_seconds
        super().save(*args, **kwargs)

    def __str__(self):
        p2_name = self.player2.username if self.player2 else "Waiting..."
        return f"Battle [{self.room_code}] {self.player1.username} vs {p2_name} ({self.status})"

class BattleEvent(models.Model):
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=50)
    data = models.TextField(blank=True, default='')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.battle.room_code} - {self.event_type} at {self.timestamp}"

class MatchmakingQueue(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='matchmaking_ticket')
    rating = models.IntegerField(default=0)
    difficulty_preference = models.CharField(max_length=10, default='ANY')
    matched_room_code = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Queue: {self.user.username} ({self.rating} pts)"
