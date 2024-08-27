from django.urls import path
from . import views
from . import chat
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('train/', views.train, name='train'),
    path('chat/', chat.chat, name='chat'),
]
