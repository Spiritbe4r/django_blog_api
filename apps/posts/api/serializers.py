from apps.comments.api.serializers import CommentSerializer
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
    )

from apps.posts.models import Post
from apps.comments.models import Comment
from apps.accounts.api.serializers import UserDetailSerializer


class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            # 'id',
            'title',
            # 'slug',
            'content',
            'publish',
        ]
post_detail_url=HyperlinkedIdentityField(
    view_name='posts-api:detail',
    lookup_field='slug')

class PostDetailSerializer(ModelSerializer):
    url=post_detail_url
    user = UserDetailSerializer(read_only=True)
    image = SerializerMethodField()
    #html=SerializerMethodField()
    comments=SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            'url',
            'id',
            'user',
            'title',
            'slug',
            'content',
            # 'html',
            'publish',
            'image',
            'comments',
        ]

    def get_image(self,obj):
        try:
            image=obj.image.url
        except:
            image=None
        return image

    def get_comments(self,obj):
        
        c_qs=Comment.objects.filter_by_instance(obj)
        comments=CommentSerializer(c_qs,many=True).data

        return comments


class PostListSerializer(ModelSerializer):
    url=post_detail_url
    user = UserDetailSerializer(read_only=True)
    class Meta:
        model = Post
        fields = [
            'url',
            'user',
            'title',
            'content',
            'publish',
        ]

