from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from configapp.models import User
from .models import Student, Teacher, Course, Group


# ✅ Foydalanuvchi (User) uchun serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "full_name", "phone", "password")
        extra_kwargs = {'password': {'write_only': True}}  # Parolni faqat yozish mumkin, o‘qish emas
        ref_name = "EducationUser"  # Konfliktni oldini olish uchun

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # Parolni xesh qilish
        return super().create(validated_data)


# ✅ Student Serializer
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Studentga bog‘langan foydalanuvchi ma’lumotlari
    courses = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=True)  # Kurslar
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())  # Guruh

    class Meta:
        model = Student
        fields = ('id', 'user', 'group', 'phone', 'courses', 'description')  # Student maydonlari
        ref_name = "EducationStudent"  # Konfliktni oldini olish uchun

    def create(self, validated_data):
        user_data = validated_data.pop('user')  # Foydalanuvchi ma’lumotlarini ajratib olish
        courses_data = validated_data.pop('courses', [])  # Kurslar ma’lumotlarini olish

        # Foydalanuvchini yaratish yoki mavjud bo‘lsa, olish
        user, created = User.objects.get_or_create(phone=user_data["phone"], defaults=user_data)

        # Studentni yaratish va kurslarini bog‘lash
        student = Student.objects.create(user=user, **validated_data)
        student.courses.set(courses_data)

        return student


# ✅ Teacher (o‘qituvchi) Serializer
class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # O‘qituvchiga bog‘langan foydalanuvchi ma’lumotlari

    class Meta:
        model = Teacher
        fields = ('id', 'user', 'subject', 'experience', 'phone', 'bio')  # O‘qituvchi maydonlari
        ref_name = "EducationTeacher"  # Konfliktni oldini olish uchun

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        # Foydalanuvchini yaratish yoki mavjud bo‘lsa, olish
        user, created = User.objects.get_or_create(phone=user_data["phone"], defaults=user_data)

        # O‘qituvchini yaratish
        teacher = Teacher.objects.create(user=user, **validated_data)

        return teacher


# ✅ Kurs bo‘yicha statistika serializeri
class CourseStatisticsSerializer(serializers.Serializer):
    course = serializers.CharField()  # Kurs nomi
    registered_count = serializers.IntegerField()  # Ro‘yxatdan o‘tgan studentlar soni
    studying_count = serializers.IntegerField()  # Hozirda o‘qiyotgan studentlar soni
    graduated_count = serializers.IntegerField()  # Bitirgan studentlar soni


# ✅ Student statistika serializeri
class StudentStatisticsSerializer(serializers.Serializer):
    course = serializers.CharField()  # Kurs nomi
    registered_count = serializers.IntegerField()  # Ro‘yxatdan o‘tgan studentlar soni
    studying_count = serializers.IntegerField()  # Hozirda o‘qiyotgan studentlar soni
    graduated_count = serializers.IntegerField()  # Bitirgan studentlar soni


# ✅ Oddiy Student Serializer (faqat ID va barcha maydonlar)
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"  # Barcha student ma’lumotlarini o‘z ichiga oladi


# ✅ Guruh (Group) serializeri
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"  # Barcha guruh ma’lumotlarini o‘z ichiga oladi
