from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from apps.accounts.models import User as usuario
from django.db.models.query_utils import Q
from rest_framework.fields import EmailField, CharField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from rest_framework.serializers import (

    HyperlinkedIdentityField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
    ValidationError)

User = usuario

class UserDetailSerializer(ModelSerializer):

    class Meta:
        model =User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]

class UserListSerializer(ModelSerializer):

    class Meta:
        model =User
        fields ='__all__'


class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='email address')
    email2 = EmailField(label='confirm email')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',

        ]
        extra_kwargs = {"password": {
            "write_only": True
        }

        }

    def validate(self, data):
        #  email=data['email']
        #  user_qs=User.objects.filter(email=email)
        # if user_qs.exists():
        #     raise ValidationError("Este Usuario ya esta Registrado")
        return data

    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get("email2")
        email2 = value
        if email1 != email2:
            raise ValidationError("Los Email no Coinciden")
        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            raise ValidationError("Este Usuario ya esta Registrado")
        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1 != email2:
            raise ValidationError("Los Email no Coinciden")
        user_qs = User.objects.filter(email=email1)
        if user_qs.exists():
            raise ValidationError("Este Usuario ya esta Registrado")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username=username,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()

        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField()
    email = EmailField(label='email address')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token',

        ]
        extra_kwargs = {"password"
                        : {"write_only": True}
                        }

    def validate(self, data):
        user_obj=None
        email=data.get("email",None)
        username=data.get("username",None)
        password=data.get["passoword"]
        if not email and not username:
            raise ValidationError("A username or email is required to login")
        user=User.objects.filter(
            Q(email=email)|
            Q(username=username)
        ).distinct()
        user=user.exclude(email__isnull=True).exclude(email__iexact='')
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials please try again")

        data["token"]="SOME RANDOM TOKEN"
        return data

class UserTokenSerializer(ModelSerializer):
    class Meta:
        model= User
        fields=('username','email','name','last_name')

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'name', 'last_name')
        extra_kwargs = {
            'name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

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