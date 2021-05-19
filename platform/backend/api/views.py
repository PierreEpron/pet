from rest_framework import viewsets, permissions
from .models import ExamWording, ExamRoom, Exam
from .serializers import ExamWordingSerializer, ExamRoomSerializer, ExamSerializer

class ExamWordingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ExamWording to be viewed or edited.
    """
    queryset = ExamWording.objects.all().order_by('-modified_date')
    serializer_class = ExamWordingSerializer
    # permission_classes = [permissions.IsAuthenticated]

class ExamRoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ExamRoom to be viewed or edited.
    """
    queryset = ExamRoom.objects.all().order_by('-modified_date')
    serializer_class = ExamRoomSerializer
    # permission_classes = [permissions.IsAuthenticated]

class ExamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows exam to be viewed or edited.
    """
    queryset = Exam.objects.all().order_by('-modified_date')
    serializer_class = ExamSerializer
    # permission_classes = [permissions.IsAuthenticated]
