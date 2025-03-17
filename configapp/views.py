from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from configapp.models import Student, Course, Teacher
from configapp.serializers import (
    StudentStatisticsSerializer,
    StudentCreateSerializer,
    TeacherSerializer
)
from rest_framework import generics


# ✅ O‘qituvchi yaratish uchun API (CreateAPIView avtomatik ravishda POST so‘rovni qo‘llab-quvvatlaydi)
class TeacherCreateAPIView(generics.CreateAPIView):
    queryset = Teacher.objects.all()  # Barcha o‘qituvchilarni olish
    serializer_class = TeacherSerializer  # Ma'lumotlarni JSON formatga o‘tkazish uchun serializer


# ✅ Talaba yaratish uchun API
class StudentCreateAPIView(generics.CreateAPIView):
    queryset = Student.objects.all()  # Barcha talabalarni olish
    serializer_class = StudentCreateSerializer  # Talaba yaratish uchun serializer


# ✅ Talabalar statistikasi uchun API
class StudentStatisticsAPIView(APIView):
    def get(self, request):
        date1 = request.GET.get("date1")  # So‘rovdan `date1` qiymatini olish
        date2 = request.GET.get("date2")  # So‘rovdan `date2` qiymatini olish

        students = Student.objects.all()  # Barcha talabalarni olish
        if date1 and date2:
            students = students.filter(created__range=[date1, date2])  # Berilgan sanalar oralig‘idagi talabalarni filtr qilish

        # Har bir kurs bo‘yicha talabalar statistikasi
        statistics = [
            {
                "course": course.name,  # Kurs nomi
                "registered_count": students.filter(courses=course).count(),  # Ro‘yxatdan o‘tgan talabalar soni
                "studying_count": students.filter(courses=course, graduated=False).count(),  # Hozirda o‘qiyotgan talabalar soni
                "graduated_count": students.filter(courses=course, graduated=True).count()  # Bitirgan talabalar soni
            }
            for course in Course.objects.all()  # Barcha kurslar uchun ushbu statistikani yaratish
        ]

        return Response({"statistics": statistics})  # JSON formatida natijani qaytarish
