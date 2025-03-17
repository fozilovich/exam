from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from configapp.views import StudentStatisticsAPIView, StudentCreateAPIView, TeacherCreateAPIView

# ✅ Swagger konfiguratsiyasi
schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="admin@example.com"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # API'lar
    path("api/", include("education.urls")),
    path("students/statistics/", StudentStatisticsAPIView.as_view(), name="student-statistics"),
    path("students/create/", StudentCreateAPIView.as_view(), name="student-create"),
    path("teachers/create/", TeacherCreateAPIView.as_view(), name="teacher-create"),

    # Swagger hujjatlari
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
