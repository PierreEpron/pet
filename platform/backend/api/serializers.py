from rest_framework import serializers
from .models import Document, DocumentToApply

class ContentSerializer(serializers.ModelSerializer):
    FIELDS = ['id', 'modified_by', 'created_by', 'created_date' , 'modified_date']
    id = serializers.ReadOnlyField()
    
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

def valid_list_of_dict(value, error_msg, callback):
    for v in value:
        if not isinstance(v, dict):
            raise serializers.ValidationError(error_msg)
        callback(v)

def valid_exist_type(value, newValue, obj, key, type):
    if key not in value or not isinstance(value[key], type):
        raise serializers.ValidationError(f"{obj}.{key} missing or should be a {type}.")
    newValue[key] = value[key]

def valid_feature(value):
    newValue = {}
    valid_exist_type(value, newValue, 'feature', 'name', str)
    valid_exist_type(value, newValue, 'feature', 'sources', list)
    value = newValue
    valid_list_of_dict(value['sources'], 'sources should be a list of dict', valid_source)

def valid_source(value):
    newValue = {}
    valid_exist_type(value, newValue, 'source', 'name', str)
    valid_exist_type(value, newValue, 'source', 'type', str)
    valid_exist_type(value, newValue, 'source', 'items', list)
    value = newValue
    valid_list_of_dict(value['items'], 'items should be a list of dict', valid_item)

def valid_item(value):
    newValue = {}

    valid_exist_type(value, newValue, 'item', 'label', str)
    
    if 'start' in value and 'end' in value:
        if not isinstance(value['start'], int):
            raise serializers.ValidationError("item.start should be an int.")
        if not isinstance(value['end'], int):
            raise serializers.ValidationError("item.end should be an int.")

        newValue['start'] = value['start']
        newValue['end'] = value['end']

    if 'probability' in value:
        # if not isinstance(value, float):
        #     raise serializers.ValidationError("item.probability should be an float.")

        newValue['probability'] = value['probability']

    value = newValue

class DocumentSerializer(ContentSerializer):
    class Meta:
        model = Document
        fields = ['title', 'text', 'features','stats'] + ContentSerializer.FIELDS

    def validate_features(self, value):
        """
        Check and filter value of features.
        """
        if not isinstance(value, list):
            raise serializers.ValidationError("Features should be a list.")

        valid_list_of_dict(value, 'features should be a list of dict', valid_feature)
                    
        return value

