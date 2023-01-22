from django.urls import path
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


# schema_view = get_schema_view(
#    openapi.Info(
#       title="Django Movie",
#       default_version='v1',
#       description="Test description",
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [

path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
  
]

