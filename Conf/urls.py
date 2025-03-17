from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import JsonResponse

# Swagger konfiguratsiyasi
schema_view = get_schema_view(
    openapi.Info(
        title="Education API",
        default_version='v1',
        description="Education API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Bosh sahifa uchun oddiy endpoint
def home(request):
    return JsonResponse({"message": "Welcome to API!"})



# URL'lar ro'yxati
urlpatterns = [
    path("", home, name="home"),
    path("api/", include("education.urls")),  # Education API yo‘llari
    path("api/", include("configapp.urls")),  # API uchun `configapp` ichidagi yo'llar
    path("admin/", admin.site.urls),  # Admin panel
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger UI
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # ReDoc hujjatlari
]


