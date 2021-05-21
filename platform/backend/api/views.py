from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from .models import ExamWording, ExamRoom, Exam, ExamReport
from .serializers import ExamWordingSerializer, ExamRoomSerializer, ExamSerializer, ExamReportSerializer

class ContentViewSet(viewsets.ModelViewSet):
    FILTERSET_FIELDS = ['modified_by', 'created_by', 'created_date' , 'modified_date']

    filter_backends = [DjangoFilterBackend]

    def get_serializer(self, *args, **kwargs):
        if isinstance(self.request.data, list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

class ExamWordingViewSet(ContentViewSet):
    """
    API endpoint that allows ExamWording to be viewed or edited.
    """
    queryset = ExamWording.objects.all().order_by('-modified_date')
    serializer_class = ExamWordingSerializer
    # permission_classes = [permissions.IsAuthenticated]

    filterset_fields = ['word'] + ContentViewSet.FILTERSET_FIELDS

class ExamRoomViewSet(ContentViewSet):
    """
    API endpoint that allows ExamRoom to be viewed or edited.
    """
    queryset = ExamRoom.objects.all().order_by('-modified_date')
    serializer_class = ExamRoomSerializer

    filterset_fields = ['ref'] + ContentViewSet.FILTERSET_FIELDS
    # permission_classes = [permissions.IsAuthenticated]

class ExamViewSet(ContentViewSet):
    """
    API endpoint that allows Exam to be viewed or edited.
    """
    queryset = Exam.objects.all().order_by('-modified_date')
    serializer_class = ExamSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['ref', 'date', 'wording', 'room'] + ContentViewSet.FILTERSET_FIELDS

class ExamReportViewSet(ContentViewSet):
    """
    API endpoint that allows ExamReport to be viewed or edited.
    """
    queryset = ExamReport.objects.all().order_by('-modified_date')
    serializer_class = ExamReportSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['text', 'exam'] + ContentViewSet.FILTERSET_FIELDS