from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import Student, Teacher, Course
from .serializers import StudentSerializer, TeacherSerializer, CourseStatisticsSerializer
from .pagination import StudentPagination
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Student, Group
from .serializers import StudentSerializer, GroupSerializer
from django.utils.dateparse import parse_date
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student, Course


# ✅ Studentni filterlash uchun API
class StudentFilterView(APIView):
    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get("start_date")  # Boshlanish sanasi
        end_date = request.query_params.get("end_date")  # Tugash sanasi
        status = request.query_params.get("status")  # Holat (studying, graduated, admitted)

        if not start_date or not end_date:
            return Response({"error": "start_date va end_date berilishi kerak"}, status=400)

        start_date = parse_date(start_date)
        end_date = parse_date(end_date)

        if not start_date or not end_date:
            return Response({"error": "start_date yoki end_date noto‘g‘ri formatda"}, status=400)

        students = Student.objects.filter(enrollment_date__range=[start_date, end_date])

        if status:
            students = students.filter(status__iexact=status)  # Holat bo‘yicha filter

        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


# ✅ Studentlar uchun ViewSet (CRUD)
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = StudentPagination  # Pagination qo‘shilgan


# ✅ Student yaratish uchun API
class StudentCreateView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# ✅ O‘qituvchilar uchun ViewSet (CRUD)
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


# ✅ O‘qituvchi yaratish uchun API
class TeacherCreateView(generics.CreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


# ✅ Studentlar statistikasi API
class StudentStatisticsAPIView(APIView):
    def get(self, request):
        date1 = request.GET.get("date1")  # Boshlanish sanasi
        date2 = request.GET.get("date2")  # Tugash sanasi

        students = Student.objects.all()
        if date1 and date2:
            students = students.filter(user__created__range=[date1, date2])  # Sanalar orasida filter

        statistics = [
            {
                "course": course.name,
                "registered_count": students.filter(courses=course).count(),  # Ro‘yxatdan o‘tganlar
                "studying_count": students.filter(courses=course, graduated=False).count(),  # Hozirda o‘qiyotganlar
                "graduated_count": students.filter(courses=course, graduated=True).count(),  # Bitirganlar
            }
            for course in Course.objects.all()
        ]

        return Response({"statistics": statistics})


# ✅ Kurslar statistikasi API
class CourseStatisticsAPIView(APIView):
    def get(self, request):
        date1 = request.GET.get("date1")  # Boshlanish sanasi
        date2 = request.GET.get("date2")  # Tugash sanasi

        date1 = parse_date(date1) if date1 else None
        date2 = parse_date(date2) if date2 else None

        students = Student.objects.all()
        if date1 and date2:
            students = students.filter(created_at__range=[date1, date2])  # Sanalar oralig‘ida filter

        statistics = [
            {
                "course": course.name,
                "registered_count": students.filter(courses=course).count(),  # Ro‘yxatdan o‘tganlar
                "studying_count": students.filter(courses=course, status="studying").count(),  # Hozirda o‘qiyotganlar
                "graduated_count": students.filter(courses=course, status="graduated").count(),  # Bitirganlar
            }
            for course in Course.objects.all()
        ]

        return Response({"statistics": statistics})


# ✅ Student statistikasi bo‘yicha API
class StudentStatisticsView(APIView):
    def get(self, request):
        return Response({"message": "Student statistics data"})


# ✅ Talabalarni ID bo‘yicha olish API
@swagger_auto_schema(
    method='post',
    operation_description="Talabalar ro‘yxatini ID bo‘yicha olish",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "student_ids": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER))
        },
        required=["student_ids"],
    ),
    responses={200: StudentSerializer(many=True)}
)
@api_view(["POST"])
def get_students(request):
    student_ids = request.data.get("student_ids", [])  # So‘rovdan IDlarni olish
    students = Student.objects.filter(id__in=student_ids)  # ID bo‘yicha filter
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)


# ✅ Guruhlarni ID bo‘yicha olish API
@swagger_auto_schema(
    method='post',
    operation_description="Guruhlar ro‘yxatini ID bo‘yicha olish",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "group_ids": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER))
        },
        required=["group_ids"],
    ),
    responses={200: GroupSerializer(many=True)}
)
@api_view(["POST"])
def get_groups(request):
    group_ids = request.data.get("group_ids", [])  # So‘rovdan IDlarni olish
    groups = Group.objects.filter(id__in=group_ids)  # ID bo‘yicha filter
    serializer = GroupSerializer(groups, many=True)
    return Response(serializer.data)
