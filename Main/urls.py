from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/', views.chat, name='chat'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    
    path('message/', views.message, name='message'),
    path('messages/', views.messages, name='messages'),
    path('next_chat/', views.next_chat, name='next_chat'),
    path('chat_info/', views.chat_info, name='chat_info'),
    path('disconnect/', views.disconnect, name='disconnect'),
    path('typeing/on/', views.typeing, name="typeing-on"),
    path('typeing/off/', views.not_typeing, name="typeing-off"),
    path('favicon.ico', views.favicon, name="favicon"),
    path('map', views.map, name="map"),
    
]