from django.db import models
from rest_framework import serializers
from .models import ExamWording # , ExamRoom , Exam

class ContentSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['modified_by'] = None if user.is_anonymous else user
        return super().update(instance, validated_data)

class ExamWordingSerializer(ContentSerializer):
    class Meta:
        model = ExamWording
        fields = ['word', 'modified_by', 'created_by', 'created_date' , 'modified_date']


# class ExamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Exam
#         fields = ['number', 'date', 'wording_fk', 'room_fk', 'modified_date', 'modified_user']
#         read_only_fields = ['added_date', 'added_user'] 