from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import (
    StudentViewSet, TeacherViewSet, StudentCreateView, TeacherCreateView,
    CourseStatisticsAPIView, StudentStatisticsAPIView, StudentFilterView,
    get_students, get_groups
)

# ✅ Swagger sozlamalari
schema_view = get_schema_view(
    openapi.Info(
        title="Education API",
        default_version="v1",
        description="Najot Ta'lim loyihasi uchun API dokumentatsiyasi",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your-email@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# ✅ DRF router
router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='students')
router.register(r'teachers', TeacherViewSet, basename='teachers')

# ✅ URL'lar
urlpatterns = [
    path('', include(router.urls)),
    path('students/create/', StudentCreateView.as_view(), name='student-create'),
    path('students/filter/', StudentFilterView.as_view(), name='student-filter'),
    path('students/statistics/', StudentStatisticsAPIView.as_view(), name='student-statistics'),
    path('get_students/', get_students, name='get_students'),
    path('get_groups/', get_groups, name='get_groups'),
    path('course-statistics/', CourseStatisticsAPIView.as_view(), name='course-statistics'),
    path('teachers/create/', TeacherCreateView.as_view(), name='teacher-create'),

    # ✅ Swagger URL'lari
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
