from rest_framework import status
from apps.accounts.authentication_mixins import Authentication
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from apps.posts.api.pagination import PostPageNumberPagination
from apps.posts.api.permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
)
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.views import APIView
from apps.accounts.models import User as usuario

User = usuario

from .serializers import (
    RegisterSerializer,
    UserCreateSerializer,
    UserListSerializer,
    UserLoginSerializer,
)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


"""
class UserLoginAPIView(APIView):
    permission_classes=[AllowAny]

    def post(self,request,*args,**kwargs):
        data=request.data
        serializer=UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data=serializer.data
            return Response(new_data,status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)"""


class UserListCreateAPIView(Authentication, ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        user_serializer = RegisterSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(
                {"data": user_serializer.data, "msg": "Usuario creado correctamente!"},
                status=status.HTTP_201_CREATED,
            )
        return Response({'data':user_serializer.errors, "msg":"Try Again"}, status=HTTP_400_BAD_REQUEST)


"""
 def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user

        user_serializer = UserSerializer(data = request.data)
        
        # validation
        if user_serializer.is_valid():
            user_serializer.save()            
            return Response({'message':'Usuario creado correctamente!'},status = status.HTTP_201_CREATED)
        
        return Response(user_serializer.errors,status = status.HTTP_400_BAD_REQUEST)"""
