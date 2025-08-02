from django.urls import path
from . import views

app_name = 'bells'  # Пространство имен приложения

urlpatterns = [
    path('', views.bells_view, name='index'),
    path('save/', views.save_bells, name='save_bells'),  # Изменили name на 'save_bells'
    path('delete/<uuid:bell_id>/', views.delete_bell, name='delete_bell'),
    path('get_schedule/', views.get_schedule, name='get_schedule'),
]