from django.contrib import admin
from django.urls import path, include
from home.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('bells/', include('bells.urls', namespace='bells')),
    path('facepass/', include('facepass.urls', namespace='facepass')),
    path('aimodule/', include('aimodule.urls', namespace='aimodule'))
    
]
