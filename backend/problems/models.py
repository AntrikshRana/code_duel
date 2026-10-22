from django.db import models
from django.utils.text import slugify

class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ('EASY', 'Easy'),
        ('MEDIUM', 'Medium'),
        ('HARD', 'Hard'),
    ]

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='EASY')
    description = models.TextField(help_text="Detailed markdown problem statement")
    input_format = models.TextField(blank=True, default='')
    output_format = models.TextField(blank=True, default='')
    constraints = models.TextField(blank=True, default='')
    
    time_limit_sec = models.FloatField(default=2.0)
    memory_limit_mb = models.IntegerField(default=256)
    
    starter_code_python = models.TextField(default='def solve():\n    # Write your solution here\n    pass\n\nif __name__ == "__main__":\n    solve()\n')
    starter_code_cpp = models.TextField(default='#include <iostream>\nusing namespace std;\n\nint main() {\n    // Write your solution here\n    return 0;\n}\n')
    starter_code_javascript = models.TextField(default='const fs = require("fs");\n\nfunction solve() {\n    // Write your solution here\n}\n\nsolve();\n')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} [{self.difficulty}]"

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    expected_output = models.TextField()
    is_hidden = models.BooleanField(default=False, help_text="Hidden tests are strictly used for evaluation and never exposed to the client.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        visibility = "Hidden" if self.is_hidden else "Sample"
        return f"TestCase #{self.id} ({visibility}) for {self.problem.title}"
