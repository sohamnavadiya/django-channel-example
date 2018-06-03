from django.urls import path

from .views import Record
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('record/abc/', Record.as_view(), name='record'),
    path('<slug:slug>/', views.room, name='room'),
]