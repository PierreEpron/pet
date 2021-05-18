from django.db import models
from rest_framework import serializers
from .models import ExamWording # , ExamRoom , Exam


class ExamWordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamWording
        fields = ['word', 'modified_by', 'created_by', 'created_date' , 'modified_date']


# class ExamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Exam
#         fields = ['number', 'date', 'wording_fk', 'room_fk', 'modified_date', 'modified_user']
#         read_only_fields = ['added_date', 'added_user'] 