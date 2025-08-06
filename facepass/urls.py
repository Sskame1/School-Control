from django.urls import path
from . import views

app_name = 'facepass'

urlpatterns = [
    path('', views.facepass_view, name='index'),
    path('locations/', views.LocationListCreate.as_view(), name='location-list'),
    path('cameras/', views.CameraListCreate.as_view(), name='camera-list'),
    path('cameras/<int:pk>/', views.CameraDetail.as_view(), name='camera-detail'),
    path('start_recognition/', views.StartRecognitionView.as_view(), name='start-recognition'),
    path('stop_recognition/', views.StopRecognitionView.as_view(), name='stop-recognition'),
]