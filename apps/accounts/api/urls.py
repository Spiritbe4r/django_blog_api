from django.urls import path
from django.contrib import admin

from .views import (
    RegisterView,
    UserCreateAPIView,

    UserListCreateAPIView
    
)

urlpatterns = [
   # path('register/',UserCreateAPIView.as_view(),name='register'),
  #  path('login/',UserLoginAPIView.as_view(),name='login'),
    path('list/',UserListCreateAPIView.as_view(),name='users_list'),
    #path('register/', RegisterView.as_view(), name='auth_register'),
]
