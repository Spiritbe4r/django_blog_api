from django.urls import path

from .views import (
    PostListAPIView,
    PostDetailAPIView,
    PostDeleteAPIView,
    PostUpdateAPIView,
    PostCreateAPIView
)
app_name='posts_api'

urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name='list'),
    path('posts/create/', PostCreateAPIView.as_view(), name='create'),
    path('posts/<slug:slug>/', PostDetailAPIView.as_view(), name='detail'),
    path('posts/<slug:slug>/edit', PostUpdateAPIView.as_view(), name='edit'),
    path('posts/<slug:slug>/delete', PostDeleteAPIView.as_view(), name='delete'),

]
