from rest_framework import viewsets
from rest_framework import permissions
from .models import Exam, ExamWording, ExamRoom
from .serializers import ExamSerializer

class ExamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Exam.objects.all().order_by('-modified_date')
    serializer_class = ExamSerializer
    # permission_classes = [permissions.IsAuthenticated]
