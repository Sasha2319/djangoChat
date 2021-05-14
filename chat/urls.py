from django.urls import path
from . import views

urlpatterns = [
    path('', views.chats, name='chats'),
    path('<int:chat_id>/', views.chatView, name='chatView'),
]