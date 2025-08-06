from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Camera(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=15, blank=True, null=True)
    device_id = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    last_ping = models.DateTimeField(auto_now=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.location})"

class Visitor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    grade = models.CharField(max_length=10)  # Например: "9А"
    photo = models.ImageField(upload_to='visitors/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.grade})"
    
    def photo_url(self):
        if self.photo and default_storage.exists(self.photo.name):
            return self.photo.url
        return 'https://via.placeholder.com/150?text=No+Photo'

class VisitLog(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    camera = models.ForeignKey(Camera, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.visitor} - {self.timestamp}"