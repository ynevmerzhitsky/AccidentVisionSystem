from django.urls import path
from . import views

urlpatterns = [
    path('process/<int:video_id>/', views.launch_process, name='launch_process'),
]