from rest_framework import serializers
from .models import ExamWording, ExamRoom, Exam

class ContentSerializer(serializers.ModelSerializer):
    FIELDS = ['modified_by', 'created_by', 'created_date' , 'modified_date']

    def create(self, validated_data):
        user = self.context['request'].user

        if user.is_anonymous:
            validated_data['created_by'] = None
            validated_data['modified_by'] = None
        else:
            validated_data['created_by'] = user
            validated_data['modified_by'] = user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.is_anonymous:
            validated_data['modified_by'] = None  
        else:
            validated_data['modified_by'] = user
        return super().update(instance, validated_data)

class ExamWordingSerializer(ContentSerializer):
    class Meta:
        model = ExamWording
        fields = ['word'] + ContentSerializer.FIELDS

class ExamRoomSerializer(ContentSerializer):
    class Meta:
        model = ExamRoom
        fields = ['ref'] + ContentSerializer.FIELDS

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['ref', 'date', 'wording', 'room'] + ContentSerializer.FIELDS
