# models.py
from django.db import models

class Camera(models.Model):
    CAMERA_TYPES = [
        ('usb', 'USB Камера'),
        ('ip', 'IP Камера')
    ]

    name = models.CharField(max_length=100, verbose_name='Название камеры')
    camera_type = models.CharField(max_length=10, choices=CAMERA_TYPES, verbose_name='Тип камеры')
    source = models.CharField(max_length=200, verbose_name='Источник (индекс или URL)')
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name='Расположение')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Камера'
        verbose_name_plural = 'Камеры'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_camera_type_display()})"

    def get_camera_type_display(self):
        return dict(self.CAMERA_TYPES).get(self.camera_type, self.camera_type)