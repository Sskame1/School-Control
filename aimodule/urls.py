from django.urls import path
from .views import DetectionAPIView

app_name = 'aimodule'

urlpatterns = [
    path('api/detect/', DetectionAPIView.as_view(), name='detection-api'),
]