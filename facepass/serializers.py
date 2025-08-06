# serializers.py
from rest_framework import serializers
from .models import Camera

class CameraSerializer(serializers.ModelSerializer):
    camera_type_display = serializers.CharField(source='get_camera_type_display', read_only=True)
    
    class Meta:
        model = Camera
        fields = [
            'id',
            'name',
            'camera_type',
            'camera_type_display',
            'source',
            'location',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'camera_type_display']