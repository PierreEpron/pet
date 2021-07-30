from django.http.response import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from .models import Document, DocumentToApply
from .serializers import DocumentSerializer
from rest_framework.response import Response
import os, json
import requests
from helpers import correct_encoding
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.decorators import api_view
import pandas as pd
from datetime import datetime
from django.utils import timezone


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

    data = requests.post(f'{settings.MIDDLEWARE_URL}/apply',
                json.dumps({'text':document.text, 'features':document.features})
            )
    data = data.json()
    new_features = data['features']
    stats = {'word_frequencies':data['word_frequencies']}


    document = DocumentViewSet.serializer_class(document,
        context = {'request':request}, data={'features':new_features, 'stats':stats}, partial=True)

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

@api_view(['GET'])
def random_document(request):
    queryset = Document.objects.order_by("?")
    if not queryset:        
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return JsonResponse({'id':queryset.first().id})

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
                        'items': [
                            {'label':'exam_wording', 'value':item[2]},
                            {'label':'exam_room', 'value':item[3]},
                            {'label':'exam_date', 'value':str(parse_datetime(item[4], item[5]))}
                        ]
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