from django.db import models
from django.contrib.auth import get_user_model

def get_user_sentinel():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Content(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_user_model), 
        related_name='created_by', blank=True, null=True, editable=False)
    modified_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_user_model),
        related_name='modified_by', blank=True, null=True, editable=False)
    class Meta:
        abstract = True

class ExamWording(Content):
    word = models.CharField(max_length=100)

# class ExamRoom(Content):
#     name = models.CharField(max_length=6)

# class Exam(Content):
#     number = models.CharField(max_length=12)
#     date = models.DateTimeField()
#     wording_fk = models.ForeignKey(ExamWording, on_delete=delete_handler(ExamWording))
#     room_fk = models.ForeignKey(ExamRoom, on_delete=delete_handler(ExamRoom))

