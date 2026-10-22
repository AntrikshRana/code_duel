from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Submission
from .serializers import SubmissionSerializer
from .executor import execute_submission

class SubmissionListCreateView(generics.ListCreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Submission.objects.all().select_related('user', 'problem', 'battle')
        problem_id = self.request.query_params.get('problem')
        battle_id = self.request.query_params.get('battle')
        
        if problem_id:
            queryset = queryset.filter(problem_id=problem_id)
        if battle_id:
            queryset = queryset.filter(battle_id=battle_id)
            
        return queryset

    def perform_create(self, serializer):
        # Save initially as pending with current user
        submission = serializer.save(user=self.request.user, verdict='PENDING')
        # Execute immediately
        execute_submission(submission)
        return submission

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = self.perform_create(serializer)
        return Response(SubmissionSerializer(submission).data, status=status.HTTP_201_CREATED)

class SubmissionDetailView(generics.RetrieveAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
