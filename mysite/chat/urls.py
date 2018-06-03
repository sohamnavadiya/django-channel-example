from django.urls import path

from .views import Record
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('web/record/<slug:channel_name>/', Record.as_view(), name='record'),
    path('<slug:slug>/', views.room, name='room'),
]
