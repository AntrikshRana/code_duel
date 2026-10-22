from django.db import models
from django.contrib.auth.models import User
from problems.models import Problem
from battles.models import Battle

class Submission(models.Model):
    VERDICT_CHOICES = [
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('ACCEPTED', 'Accepted'),
        ('WRONG_ANSWER', 'Wrong Answer'),
        ('TIME_LIMIT_EXCEEDED', 'Time Limit Exceeded'),
        ('COMPILATION_ERROR', 'Compilation Error'),
        ('RUNTIME_ERROR', 'Runtime Error'),
    ]

    LANGUAGE_CHOICES = [
        ('python', 'Python 3'),
        ('cpp', 'C++ 17'),
        ('javascript', 'JavaScript (Node)'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='submissions')
    battle = models.ForeignKey(Battle, on_delete=models.SET_NULL, null=True, blank=True, related_name='submissions')
    
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='python')
    code = models.TextField()
    
    verdict = models.CharField(max_length=25, choices=VERDICT_CHOICES, default='PENDING')
    execution_time_ms = models.FloatField(default=0.0)
    memory_kb = models.FloatField(default=0.0)
    test_cases_passed = models.PositiveIntegerField(default=0)
    total_test_cases = models.PositiveIntegerField(default=0)
    error_output = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Submission #{self.id} by {self.user.username} - {self.problem.title} [{self.verdict}]"
