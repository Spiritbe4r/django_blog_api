from django.urls import path
from django.contrib import admin

from .views import (
    CommentDetailAPIView,
    CommentListAPIView,
    CommentCreateAPIView,
   # CommentEditAPIView

    )

urlpatterns = [
    path('', CommentListAPIView.as_view(), name='list'),
    path('<int:pk>/',CommentDetailAPIView.as_view(), name='thread'),
    path('create/', CommentCreateAPIView.as_view(), name='create'),
  #  path('<int:pk>/edit',CommentEditAPIView.as_view(), name='edit'),
] 
