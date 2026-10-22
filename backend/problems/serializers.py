from rest_framework import serializers
from .models import Problem, TestCase

class SampleTestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ['id', 'input_data', 'expected_output', 'order']

class ProblemListSerializer(serializers.ModelSerializer):
    submissions_count = serializers.SerializerMethodField()
    acceptance_rate = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = ['id', 'title', 'slug', 'difficulty', 'time_limit_sec', 'memory_limit_mb', 'submissions_count', 'acceptance_rate']

    def get_submissions_count(self, obj):
        return obj.submissions.count()

    def get_acceptance_rate(self, obj):
        total = obj.submissions.count()
        if total == 0:
            return 0
        accepted = obj.submissions.filter(verdict='ACCEPTED').count()
        return round((accepted / total) * 100, 1)

class ProblemDetailSerializer(serializers.ModelSerializer):
    sample_tests = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = [
            'id', 'title', 'slug', 'difficulty', 'description',
            'input_format', 'output_format', 'constraints',
            'time_limit_sec', 'memory_limit_mb',
            'starter_code_python', 'starter_code_cpp', 'starter_code_javascript',
            'sample_tests'
        ]

    def get_sample_tests(self, obj):
        samples = obj.test_cases.filter(is_hidden=False)
        return SampleTestCaseSerializer(samples, many=True).data
