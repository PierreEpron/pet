from rest_framework import viewsets, permissions
from .models import ExamWording, ExamRoom, Exam, ExamReport
from .serializers import ExamWordingSerializer, ExamRoomSerializer, ExamSerializer, ExamReportSerializer

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
    API endpoint that allows Exam to be viewed or edited.
    """
    queryset = Exam.objects.all().order_by('-modified_date')
    serializer_class = ExamSerializer
    # permission_classes = [permissions.IsAuthenticated]

class ExamReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ExamReport to be viewed or edited.
    """
    queryset = ExamReport.objects.all().order_by('-modified_date')
    serializer_class = ExamReportSerializer
    # permission_classes = [permissions.IsAuthenticated]