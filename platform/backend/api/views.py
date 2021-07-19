from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from .models import Document, DocumentToApply
from .serializers import DocumentSerializer
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


def update_features(request, pk):
    report = get_object_or_404(DocumentViewSet.queryset, pk=pk)

    newFeatures = requests.post(f'{settings.MIDDLEWARE_URL}/apply',
                json.dumps({'text':report.text, 'features':report.features})
            )
    newFeatures = newFeatures.json()

    if newFeatures != report.features:
        report = DocumentViewSet.serializer_class(report, 
            context = {'request':request}, data={'features':newFeatures}, partial=True)

        if report.is_valid():
            report.save()
            DocumentToApply.objects.filter(report=pk).delete()
        else:
            print(report.errors)

class DocumentViewSet(ContentViewSet):
    """
    API endpoint that allows Document to be viewed or edited.
    """
    queryset = Document.objects.all().order_by('-modified_date')
    serializer_class = DocumentSerializer
    filterset_fields = ['text'] + ContentViewSet.FILTERSET_FIELDS

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
        # wording, _ = ExamWording.objects.get_or_create(word=item[2])
        # room, _ = ExamRoom.objects.get_or_create(ref=item[3])
        # exam, _ = Exam.objects.get_or_create(ref=item[0], defaults={
        #     'date':parse_datetime(item[4], item[5]),
        #     'wording':wording,
        #     'room':room
        # })
        report, is_new = Document.objects.get_or_create(text=correct_encoding(item[6]))
        if is_new:
            DocumentToApply.objects.get_or_create(report=report)

    return Response()

@api_view(['GET'])
def apply_queue(request):
    c = DocumentToApply.objects.count()
    if c > 0 :
        update_features(request, DocumentToApply.objects.first().report.id)
    return Response({'queue':{'count':c}})