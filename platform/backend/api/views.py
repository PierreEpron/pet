from django_filters.rest_framework import DjangoFilterBackend
from numpy.core.fromnumeric import put
from rest_framework import viewsets, permissions
from rest_framework.serializers import Serializer
from .models import ExamWording, ExamRoom, Exam, ExamReport
from .serializers import ExamWordingSerializer, ExamRoomSerializer, ExamSerializer, ExamReportSerializer
from rest_framework.response import Response
import os, json
import requests

class ContentViewSet(viewsets.ModelViewSet):
    FILTERSET_FIELDS = ['modified_by', 'created_by', 'created_date' , 'modified_date']
    filter_backends = [DjangoFilterBackend]
    permission_classes = [] if os.environ.get("SECURITY", "0") == "0" else [permissions.IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if isinstance(self.request.data, list):
            kwargs['many'] = True

        self.serializer_class.Meta.depth = int(self.request.GET.get('depth', 0))

        return super().get_serializer(*args, **kwargs)

class ExamWordingViewSet(ContentViewSet):
    """
    API endpoint that allows ExamWording to be viewed or edited.
    """
    queryset = ExamWording.objects.all().order_by('-modified_date')
    serializer_class = ExamWordingSerializer

    filterset_fields = ['word'] + ContentViewSet.FILTERSET_FIELDS

class ExamRoomViewSet(ContentViewSet):
    """
    API endpoint that allows ExamRoom to be viewed or edited.
    """
    queryset = ExamRoom.objects.all().order_by('-modified_date')
    serializer_class = ExamRoomSerializer

    filterset_fields = ['ref'] + ContentViewSet.FILTERSET_FIELDS

class ExamViewSet(ContentViewSet):
    """
    API endpoint that allows Exam to be viewed or edited.
    """
    queryset = Exam.objects.all().order_by('-modified_date')
    serializer_class = ExamSerializer
    filterset_fields = ['ref', 'date', 'wording', 'room'] + ContentViewSet.FILTERSET_FIELDS

class ExamReportViewSet(ContentViewSet):
    """
    API endpoint that allows ExamReport to be viewed or edited.
    """
    queryset = ExamReport.objects.all().order_by('-modified_date')
    serializer_class = ExamReportSerializer
    filterset_fields = ['text', 'exam'] + ContentViewSet.FILTERSET_FIELDS

    def retrieve(self, request, pk=None):
        exam_report = super().retrieve(self, request, pk)
        res = requests.post('http://172.19.0.4:5000/apply',
            json.dumps({'text':exam_report.data['text'], 'features':exam_report.data['features']})
        )
        return exam_report

from rest_framework.decorators import api_view
import pandas as pd
from datetime import datetime
from django.utils import timezone

def parse_datetime(date, time):
    date = date.split('/')
    time = time.split(':')
    return timezone.make_aware(datetime(int('20' + date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1])))    

@api_view(['POST'])
def upload(request):
    data = pd.read_csv(request.data['csv'], sep='\t')
    for item in data.values:
        wording, _ = ExamWording.objects.get_or_create(word=item[2])
        room, _ = ExamRoom.objects.get_or_create(ref=item[3])
        exam, _ = Exam.objects.get_or_create(ref=item[0], defaults={
            'date':parse_datetime(item[4], item[5]),
            'wording':wording,
            'room':room
        })
        ExamReport.objects.get_or_create(text=item[6], exam=exam)

    return Response({"message": "Hello, world!"})