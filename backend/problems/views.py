from rest_framework import generics, permissions
from .models import Problem
from .serializers import ProblemListSerializer, ProblemDetailSerializer

class ProblemListView(generics.ListAPIView):
    queryset = Problem.objects.all().order_by('id')
    serializer_class = ProblemListSerializer
    permission_classes = [permissions.AllowAny]

class ProblemDetailView(generics.RetrieveAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'
