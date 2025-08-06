# urls.py
from django.urls import path
from . import views

app_name = 'facepass'

urlpatterns = [
    path('', views.facepass_view, name='index'),
    path('api/usb-cameras/', views.USBCamerasAPIView.as_view(), name='usb-cameras'),
    path('api/cameras/', views.CameraAPIView.as_view(), name='cameras-list'),
    path('api/cameras/<int:pk>/', views.CameraDetailAPIView.as_view(), name='camera-detail'),
    path('camera_stream/<int:camera_id>/', views.camera_stream, name='camera-stream'),
]