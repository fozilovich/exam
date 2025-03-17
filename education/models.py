from django.db import models
from configapp.models import User, Course, Group
from django.utils import timezone

# ✅ Student modeli
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='education_student')  # Foydalanuvchi bilan bog'lanish (1:1 munosabat)
    courses = models.ManyToManyField(Course, related_name='education_students', blank=True)  # Talaba bir nechta kursga yozilishi mumkin (ManyToMany)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='education_students')  # Talabaning guruhi (ForeignKey)
    description = models.TextField(null=True, blank=True)  # Qo‘shimcha izoh maydoni
    status = models.CharField(
        max_length=20,
        choices=[("studying", "Studying"), ("graduated", "Graduated")],  # Talabaning holati (o‘qiyapti yoki bitirgan)
        default="studying"
    )
    created_at = models.DateTimeField(default=timezone.now)  # Talaba qachon yaratilganligini saqlash

    def __str__(self):
        return self.user.phone if self.user else "No User"  # Foydalanuvchi telefon raqami qaytariladi


# ✅ Teacher modeli
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='education_teacher')  # Foydalanuvchi bilan bog'lanish (1:1 munosabat)
    subject = models.CharField(max_length=100)  # O‘qituvchining darsi
    experience = models.IntegerField()  # Tajriba yillari
    phone = models.CharField(max_length=15, unique=True)  # Telefon raqami (takrorlanmas bo‘lishi kerak)
    bio = models.TextField()  # Qo‘shimcha ma’lumotlar (biografiya)

    def __str__(self):
        return self.user.phone if self.user else "No User"  # O‘qituvchi telefon raqami qaytariladi
