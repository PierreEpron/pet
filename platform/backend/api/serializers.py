from rest_framework import serializers
from .models import Exam, ExamWording, ExamRoom

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['number', 'date', 'wording_fk', 'room_fk', 'added_date', 
            'modified_date', 'added_user', 'modified_user']