# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import cv2
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Camera
from .serializers import CameraSerializer
from django.http import StreamingHttpResponse, HttpResponse
import threading
from aimodule.views import get_detection_result

camera_threads = {}

class VideoCamera(object):
    def __init__(self, camera_index):
        self.video = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

class USBCamerasAPIView(APIView):
    def get(self, request):
        """API для получения списка доступных USB камер"""
        def get_connected_usb_cameras():
            cameras = []
            for i in range(10):
                try:
                    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
                    if cap.isOpened():
                        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        cameras.append({
                            'index': i,
                            'name': f'USB Camera {i}',
                            'resolution': f"{width}x{height}"
                        })
                        cap.release()
                except Exception as e:
                    continue
            return cameras

        try:
            cameras = get_connected_usb_cameras()
            return Response({
                'success': True,
                'cameras': cameras,
                'message': f"Найдено {len(cameras)} USB камер"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': f"Ошибка при поиске камер: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CameraAPIView(ListCreateAPIView):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

class CameraDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

def camera_stream(request, camera_id):
    try:
        camera = Camera.objects.get(pk=camera_id)
        if camera.camera_type == 'usb':
            camera_index = int(camera.source)
        else:
            # Для сетевых камер
            camera_index = camera.source
            
        if camera_id not in camera_threads:
            camera_threads[camera_id] = VideoCamera(camera_index)
            
        return StreamingHttpResponse(gen(camera_threads[camera_id]),
                            content_type='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(f"Error in camera_stream: {str(e)}")
        return HttpResponse(status=500)

def facepass_view(request):
    return render(request, 'facepass/index.html')