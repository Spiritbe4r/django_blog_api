from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, CreateAPIView, \
    RetrieveUpdateAPIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)

from apps.posts.api.pagination import PostPageNumberPagination
from apps.posts.api.permissions import IsOwnerOrReadOnly
from apps.posts.api.serializers import PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer
from apps.posts.models import Post

class PostCreateAPIView(CreateAPIView):
    queryset=Post.objects.all()
    serializer_class=PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

class PostListAPIView(ListAPIView):

    serializer_class=PostListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields=['title','content','user__first_name']
    pagination_class = PostPageNumberPagination #pageNumberpagination
    def get_queryset(self,*args,**kwargs):
        queryset_list = Post.objects.all()
        query=self.request.GET.get("q")
        if query:
            queryset_list=queryset_list.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()

        return queryset_list

class PostDetailAPIView(RetrieveAPIView):
    queryset=Post.objects.all()
    serializer_class=PostDetailSerializer
    lookup_field='slug'

class PostDeleteAPIView(DestroyAPIView):
    queryset=Post.objects.all()
    serializer_class=PostDetailSerializer
    lookup_field='slug'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]

class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset=Post.objects.all()
    serializer_class=PostCreateUpdateSerializer
    lookup_field='slug'
    permission_classes = [IsOwnerOrReadOnly,IsAuthenticatedOrReadOnly]
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)