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
    document = get_object_or_404(DocumentViewSet.queryset, pk=pk)

    newFeatures = requests.post(f'{settings.MIDDLEWARE_URL}/apply',
                json.dumps({'text':document.text, 'features':document.features})
            )
    newFeatures = newFeatures.json()

    if newFeatures != document.features:
        document = DocumentViewSet.serializer_class(document, 
            context = {'request':request}, data={'features':newFeatures}, partial=True)

        if document.is_valid():
            document.save()
            DocumentToApply.objects.filter(document=pk).delete()
        else:
            print(document.errors)

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

        if not Document.objects.filter(title=item[0], text=correct_encoding(item[6])):
            document = DocumentSerializer(context = {'request':request}, data=
            {
                'title':item[0],
                'text':item[6],
                'created_by': request.user, 
                'features': [{'name':'meta', 
                    'sources': [{
                        'name': request.user.username,
                        'type': 'model',
                        'items': []
                    }]
                }]
            })
            if document.is_valid():
                DocumentToApply.objects.get_or_create(document=document.save())
            else:
                print(document.errors)
                
    return Response()

@api_view(['GET'])
def apply_queue(request):
    c = DocumentToApply.objects.count()
    if c > 0 :
        update_features(request, DocumentToApply.objects.first().document.id)
    return Response({'queue':{'count':c}})