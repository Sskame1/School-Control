from django.shortcuts import render
from .models import Camera, VisitLog, Visitor, Location
from .serializers import LocationSerializer, CameraSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import cv2

class LocationListCreate(ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class CameraListCreate(ListCreateAPIView):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CameraDetail(RetrieveUpdateDestroyAPIView):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

class StartRecognitionView(APIView):
    def post(self, request):
        camera_id = request.data.get('camera_id')
        # Здесь будет логика запуска распознавания
        return Response({'status': 'success'}, status=status.HTTP_200_OK)

class StopRecognitionView(APIView):
    def post(self, request):
        # Здесь будет логика остановки распознавания
        return Response({'status': 'success'}, status=status.HTTP_200_OK)

def get_usb_cameras():
    usb_cameras = []
    for i in range(3):  # Проверяем только первые 3 индекса
        try:
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if cap.isOpened():
                usb_cameras.append({
                    'index': i,
                    'name': f'USB Camera {i}',
                    'resolution': f'{int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}'
                })
                cap.release()
        except Exception as e:
            print(f"Error checking camera index {i}: {str(e)}")
            continue
    return usb_cameras

def facepass_view(request):
    try:
        usb_cameras = get_usb_cameras()
    except Exception as e:
        print(f"Error getting USB cameras: {e}")
        usb_cameras = []
    
    context = {
        'cameras': Camera.objects.filter(is_active=True),
        'recent_visits': VisitLog.objects.all().order_by('-timestamp')[:10],
        'all_visitors': Visitor.objects.all(),
        'locations': Location.objects.all(),
        'usb_cameras': usb_cameras,
    }
    return render(request, 'facepass/index.html', context)