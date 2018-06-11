from django.urls import path

from .views import Record, RecordAPIView
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('web/record/<slug:channel_name>/', RecordAPIView.as_view(), name='record'),
    path('voice/', views.VoiceRecordTemplate.as_view()),  # Add this /index/ route
    path('<slug:slug>/', views.room, name='room'),
    path('abc/abc/', views.REDView.as_view(), name='RED'),
]
