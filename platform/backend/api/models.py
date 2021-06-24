from django.db import models
from django.contrib.auth import get_user_model

def get_user_sentinel():
    return get_user_model().objects.get_or_create(username='deleted')[0]

def get_wording_sentinel():
    return ExamWording.objects.get_or_create(username='deleted')[0]

def get_room_sentinel():
    return ExamRoom.objects.get_or_create(username='deleted')[0]

class Content(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_user_model), 
        related_name='+', blank=True, null=True, editable=False)
    modified_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_user_model),
        related_name='+', blank=True, null=True, editable=False)
    class Meta:
        abstract = True

class ExamWording(Content):
    word = models.CharField(max_length=100)

class ExamRoom(Content):
    ref = models.CharField(max_length=6)

class Exam(Content):
    ref = models.CharField(max_length=12)
    date = models.DateTimeField()
    wording = models.ForeignKey(ExamWording, on_delete=models.SET(get_wording_sentinel))
    room = models.ForeignKey(ExamRoom, on_delete=models.SET(get_room_sentinel))

class ExamReport(Content):
    text = models.TextField()
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    features = models.JSONField(null=True)