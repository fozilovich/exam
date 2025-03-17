from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

# ✅ Foydalanuvchi yaratish va boshqarish uchun Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Telefon raqam talab qilinadi!")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)  # Parolni xavfsiz saqlash
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser is_staff=True bo‘lishi kerak!")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser is_superuser=True bo‘lishi kerak!")

        return self.create_user(phone, password, **extra_fields)


# ✅ Custom User Model (Django default user modelining o‘rniga ishlatiladi)
class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex=r'^\+?998\d{9}$', message="Telefon raqam 998901234567 formatida bo‘lishi kerak.")
    phone = models.CharField(validators=[phone_regex], max_length=13, unique=True)  # Unikal telefon raqam
    full_name = models.CharField(max_length=50, null=True, blank=True)

    is_active = models.BooleanField(default=True)  # Foydalanuvchi aktiv yoki yo‘qligini tekshirish
    is_staff = models.BooleanField(default=False)  # Admin panelga kirish huquqi
    is_superuser = models.BooleanField(default=False)  # Superuser huquqlari
    is_student = models.BooleanField(default=False)  # Talaba ekanligini belgilash
    is_teacher = models.BooleanField(default=False)  # O‘qituvchi ekanligini belgilash

    created = models.DateTimeField(auto_now_add=True)  # Foydalanuvchi yaratilgan vaqt
    updated = models.DateTimeField(auto_now=True)  # Foydalanuvchi oxirgi yangilangan vaqt

    USERNAME_FIELD = 'phone'  # Login uchun telefon raqam ishlatiladi
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.full_name if self.full_name else self.phone


# ✅ Barcha modellarda qo‘llaniladigan `created` va `updated` maydonlarini ta’minlash uchun abstract model
class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)  # Yaratilgan sana
    updated = models.DateTimeField(auto_now=True)  # Oxirgi yangilangan sana

    class Meta:
        abstract = True  # Bu model faqat boshqa modellar uchun asos bo‘ladi


# ✅ Kurs modeli
class Course(BaseModel):
    name = models.CharField(max_length=255)  # Kurs nomi
    description = models.TextField(null=True, blank=True)  # Kurs tavsifi

    def __str__(self):
        return self.name


# ✅ Guruh modeli
class Group(BaseModel):
    name = models.CharField(max_length=255)  # Guruh nomi
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="groups")  # Qaysi kursga tegishli

    def __str__(self):
        return f"{self.name} ({self.course.name})"


# ✅ Talaba modeli
class Student(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")  # Har bir talabaga bitta user
    courses = models.ManyToManyField(Course, related_name="students", blank=True)  # Talabaning kurslari
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="students")  # Talaba guruhga tegishli
    description = models.TextField(null=True, blank=True)  # Qo‘shimcha tavsif
    graduated = models.BooleanField(default=False)  # Bitirgan yoki yo‘q

    def __str__(self):
        return self.user.full_name if self.user.full_name else self.user.phone


# ✅ O‘qituvchi modeli
class Teacher(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')  # O‘qituvchi user bilan bog‘langan
    courses = models.ManyToManyField(Course, related_name='teachers', blank=True)  # O‘qituvchi dars beradigan kurslar
    bio = models.TextField(null=True, blank=True)  # O‘qituvchining tavsifi

    def __str__(self):
        return self.user.full_name if self.user.full_name else self.user.phone
