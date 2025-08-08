import cv2
import numpy as np
from PIL import Image, ImageOps
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

# Загрузка модели и меток (вынесено в глобальную область для однократной загрузки)
model = None
class_names = []

def load_ai_model():
    global model, class_names
    if model is None:
        from keras.models import load_model
        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)
        # Load the model
        model = load_model("aimodule/models/keras_Model.h5", compile=False)
        # Load the labels
        class_names = open("aimodule/models/labels.txt", "r").readlines()

def get_detection_result(frame):
    """
    Обрабатывает кадр с камеры и возвращает результат детекции
    Возвращает:
    - обработанный кадр (с наложенными метками)
    - название класса
    - уровень уверенности
    """
    load_ai_model()  # Убедимся, что модель загружена
    
    # Преобразуем кадр из BGR (OpenCV) в RGB (Pillow)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(rgb_frame)
    
    # Подготовка изображения для модели
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    
    # Создаем массив для предсказания
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array
    
    # Делаем предсказание
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()[2:]  # Убираем лишние символы
    confidence_score = float(prediction[0][index])
    
    # Добавляем текст на кадр
    label = f"{class_name}: {confidence_score:.2f}"
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    return frame, class_name, confidence_score

class DetectionAPIView(APIView):
    """
    API для обработки одного изображения
    """
    def post(self, request):
        if 'image' not in request.FILES:
            return Response({"error": "No image provided"}, status=400)
        
        try:
            # Читаем изображение из запроса
            image_file = request.FILES['image']
            image = Image.open(image_file).convert('RGB')
            
            # Преобразуем в numpy array (OpenCV формат)
            frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Получаем результат детекции
            processed_frame, class_name, confidence = get_detection_result(frame)
            
            # Преобразуем обработанный кадр в base64 для ответа
            _, buffer = cv2.imencode('.jpg', processed_frame)
            encoded_image = buffer.tobytes()
            
            return Response({
                "class": class_name,
                "confidence": confidence,
                "processed_image": encoded_image
            })
            
        except Exception as e:
            return Response({"error": str(e)}, status=500)