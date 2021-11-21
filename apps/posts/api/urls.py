from django.urls import path

from .views import (
    PostListAPIView,
    PostDetailAPIView,
    PostDeleteAPIView,
    PostUpdateAPIView,
    PostCreateAPIView
)

urlpatterns = [
    path('', PostListAPIView.as_view(), name='list'),
    path('create/', PostCreateAPIView.as_view(), name='create'),
    path('<slug:slug>/', PostDetailAPIView.as_view(), name='detail'),
    path('<slug:slug>/edit', PostUpdateAPIView.as_view(), name='edit'),
    path('<slug:slug>/delete', PostDeleteAPIView.as_view(), name='delete'),

]
