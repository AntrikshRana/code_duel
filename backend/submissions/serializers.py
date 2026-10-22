from rest_framework import serializers
from .models import Submission

class SubmissionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    problem_title = serializers.CharField(source='problem.title', read_only=True)

    class Meta:
        model = Submission
        fields = [
            'id', 'user', 'username', 'problem', 'problem_title', 'battle',
            'language', 'code', 'verdict', 'execution_time_ms', 'memory_kb',
            'test_cases_passed', 'total_test_cases', 'error_output', 'created_at'
        ]
        read_only_fields = ['user', 'verdict', 'execution_time_ms', 'memory_kb', 'test_cases_passed', 'total_test_cases', 'error_output']
