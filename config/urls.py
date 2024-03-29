"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from apps.accounts.api.views import RegisterView
# from rest_framework_jwt.views import obtain_jwt_token
from django.contrib import admin
from django.urls import path,include

from .yasg import urlpatterns as doc_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    #  path('base/', include(('apps.base.urls','posts-api'))),
    # path('', include("apps.posts.urls", namespace='posts')),
    path('api/comments/',include(('apps.comments.api.urls','comments-api'))),
    path('api/',include('apps.posts.api.urls',namespace='posts-api')),
    path('api/users/',include('apps.accounts.api.urls',namespace='users-api')),
    # path('api/auth/token/', obtain_jwt_token),
   
    path('register/', RegisterView.as_view(), name='auth_register'),
    
]
urlpatterns+=doc_urls