from apps.comments.api.serializers import (
    CommentDetailSerializer,
   # CommentEditSerializer,
    CommentSerializer,
    create_comment_serializar,
    
    )

from apps.comments.models import Comment
from apps.posts.api.pagination import PostPageNumberPagination
from apps.posts.api.permissions import IsOwnerOrReadOnly
from django.db.models import Q
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    CreateAPIView, 
    DestroyAPIView,
    ListAPIView, 
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView
    )
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework.mixins import DestroyModelMixin,UpdateModelMixin

class CommentCreateAPIView(CreateAPIView):
    queryset=Comment.objects.all()
   # serializer_class=PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        model_type=self.request.GET.get("type")
        slug=self.request.GET.get("slug")
        parent_id=self.request.GET.get("parent_id",None)
        return create_comment_serializar(
            model_type=model_type,
            slug=slug,
            parent_id=parent_id,
            user=self.request.user
        )

class CommentListAPIView(ListAPIView):

    serializer_class=CommentSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields=['content','user__first_name']
    pagination_class = PostPageNumberPagination #pageNumberpagination
    def get_queryset(self,*args,**kwargs):
        queryset_list = Comment.objects.all()
        query=self.request.GET.get("q")
        if query:
            queryset_list=queryset_list.filter(
                
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()

        return queryset_list


class CommentDetailAPIView(DestroyModelMixin,UpdateModelMixin,RetrieveAPIView):
    queryset=Comment.objects.filter(id__gte=0)
    serializer_class=CommentDetailSerializer
    permission_classes=[IsAuthenticated]#OrReadOnly,IsOwnerOrReadOnly]

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)
'''
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
        serializer.save(user=self.request.user)'''
