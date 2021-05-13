from django.db import models
from django.contrib.auth.models import User

def get_sentinel_wording():
    return ExamWording.objects.get_or_create(name='deleted')[0]

def get_sentinel_room():
    return ExamRoom.objects.get_or_create(name='deleted')[0]

def get_sentinel_user():
    return User.objects.get_or_create(username='deleted')[0]

class ExamWording(models.Model):
    name = models.CharField(max_length=100)

class ExamRoom(models.Model):
    name = models.CharField(max_length=6)

# Create your models here.
class Exam(models.Model):
    number = models.CharField(max_length=12)
    date = models.DateTimeField()
    wording_fk = models.ForeignKey(ExamWording, on_delete=models.SET(get_sentinel_wording))
    room_fk = models.ForeignKey(ExamRoom, on_delete=models.SET(get_sentinel_room))

    added_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    added_user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), related_name='added_user')
    modified_user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), related_name='modified_user')
