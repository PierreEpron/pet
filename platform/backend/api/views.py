from django_filters.rest_framework import DjangoFilterBackend
from numpy.core.fromnumeric import put
from rest_framework import viewsets, permissions
from rest_framework.serializers import Serializer
from .models import ExamReportToApply, ExamWording, ExamRoom, Exam, ExamReport
from .serializers import ExamWordingSerializer, ExamRoomSerializer, ExamSerializer, ExamReportSerializer
from rest_framework.response import Response
import os, json
import requests
from helpers import correct_encoding
from django.shortcuts import get_object_or_404
from django.conf import settings

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

def update_features(request, pk):
    report = get_object_or_404(ExamReportViewSet.queryset, pk=pk)

    newFeatures = requests.post(f'{settings.MIDDLEWARE_URL}/apply',
                json.dumps({'text':report.text, 'features':report.features})
            )
    print(newFeatures)
    newFeatures = newFeatures.json()

    if newFeatures != report.features:
        report = ExamReportViewSet.serializer_class(report, 
            context = {'request':request}, data={'features':newFeatures}, partial=True)

        if report.is_valid():
            report.save()
            ExamReportToApply.objects.filter(report=pk).delete()
        else:
            print(report.errors)

class ExamReportViewSet(ContentViewSet):
    """
    API endpoint that allows ExamReport to be viewed or edited.
    """
    queryset = ExamReport.objects.all().order_by('-modified_date')
    serializer_class = ExamReportSerializer
    filterset_fields = ['text', 'exam'] + ContentViewSet.FILTERSET_FIELDS

    def retrieve(self, request, pk=None):
        
        update_features(request, pk)

        return super().retrieve(self, request, pk)

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
    data = pd.read_csv(request.data['csv'], sep='\t', encoding='utf-8')
    for item in data.values:
        wording, _ = ExamWording.objects.get_or_create(word=item[2])
        room, _ = ExamRoom.objects.get_or_create(ref=item[3])
        exam, _ = Exam.objects.get_or_create(ref=item[0], defaults={
            'date':parse_datetime(item[4], item[5]),
            'wording':wording,
            'room':room
        })
        
        report, is_new = ExamReport.objects.get_or_create(text=correct_encoding(item[6]), exam=exam)
        if is_new:
            ExamReportToApply.objects.get_or_create(report=report)
    return Response()

@api_view(['GET'])
def apply_queue(request):
    c = ExamReportToApply.objects.count()
    if c > 0 :
        update_features(request, ExamReportToApply.objects.first().report.id)
    return Response({'queue':{'count':c}})