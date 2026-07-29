from django.urls import path
from . import views

name='chat'

urlpatterns = [
    path('', views.chat_room, name='chat'),
]