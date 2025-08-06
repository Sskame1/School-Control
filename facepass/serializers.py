from rest_framework import serializers
from .models import Location, Camera

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'description']

class CameraSerializer(serializers.ModelSerializer):
    location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Camera
        fields = ['id', 'name', 'ip_address', 'port', 'device_id', 'is_active', 'location', 'type']
        extra_kwargs = {
            'device_id': {'required': False},
            'ip_address': {'required': False},
            'port': {'required': False}
        }