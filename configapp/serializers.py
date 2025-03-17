from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from configapp.models import User, Course, Group, Student, Teacher


# ✅ Foydalanuvchi (User) Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "full_name", "phone", "password")  # Foydalanuvchi ma'lumotlari
        extra_kwargs = {"password": {"write_only": True}}  # Parol faqat yozish uchun (ko‘rsatilmaydi)
        ref_name = "ConfigAppUser"  # Serializer nomi konflikt bo‘lmasligi uchun

    def create(self, validated_data):
        """Parolni hash holatida saqlash"""
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


# ✅ Talaba yaratish uchun Serializer
class StudentCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Talaba bilan bog‘liq foydalanuvchi ma'lumotlari

    class Meta:
        model = Student
        fields = ["id", "user", "group", "courses", "description"]  # Talaba uchun maydonlar

    def create(self, validated_data):
        """Talaba va unga bog‘liq foydalanuvchini yaratish"""
        user_data = validated_data.pop("user")  # Foydalanuvchi ma'lumotlarini ajratib olish
        user = User.objects.create(**user_data)  # Yangi foydalanuvchini yaratish
        student = Student.objects.create(user=user, **validated_data)  # Yangi talabani yaratish
        student.courses.set(validated_data["courses"])  # ManyToManyField bog‘lash
        return student


# ✅ Talabalar statistikasi uchun Serializer
class StudentStatisticsSerializer(serializers.Serializer):
    course = serializers.CharField()  # Kurs nomi
    registered_count = serializers.IntegerField()  # Ro‘yxatdan o‘tganlar soni
    studying_count = serializers.IntegerField()  # Hozirda o‘qiyotganlar soni
    graduated_count = serializers.IntegerField()  # Bitirganlar soni


# ✅ Kurslar uchun Serializer
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"  # Barcha maydonlarni olish


# ✅ Guruhlar uchun Serializer
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"  # Barcha maydonlarni olish


# ✅ O‘qituvchilar uchun Serializer
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"  # Barcha maydonlarni olish
        ref_name = "ConfigAppTeacher"  # Konfliktlarni oldini olish uchun
