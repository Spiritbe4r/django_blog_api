from django.urls import path
from django.contrib import admin

from apps.accounts.views import Login



from .views import (
    RegisterView,
    UserCreateAPIView,

    UserListCreateAPIView
    
)
app_name='users-api'

urlpatterns = [
   # path('register/',UserCreateAPIView.as_view(),name='register'),
    path('login/',Login.as_view(),name='login'),
    path('list/',UserListCreateAPIView.as_view(),name='users_list'),
    #path('register/', RegisterView.as_view(), name='auth_register'),
]
