from django_filters.rest_framework import DjangoFilterBackend
from numpy.core.fromnumeric import put
from rest_framework import viewsets, permissions
from .models import ExamWording, ExamRoom, Exam, ExamReport
from .serializers import ExamWordingSerializer, ExamRoomSerializer, ExamSerializer, ExamReportSerializer
from rest_framework.response import Response

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

from rest_framework.decorators import api_view
import numpy as np
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
    for item in data[:500].values:
        wording, _ = ExamWording.objects.get_or_create(word=item[2])
        room, _ = ExamRoom.objects.get_or_create(ref=item[3])
        exam, _ = Exam.objects.get_or_create(ref=item[0], defaults={
            'date':parse_datetime(item[4], item[5]),
            'wording':wording,
            'room':room
        })
        ExamReport.objects.get_or_create(text=item[6], exam=exam)
        print(f"{wording.id}, {room.id}, {exam.id}")        

    return Response({"message": "Hello, world!"})