from rest_framework.pagination import PageNumberPagination

# ✅ Student API uchun sahifalash (pagination) klassi
class StudentPagination(PageNumberPagination):
    page_size = 10  # Har bir sahifada ko‘rsatiladigan studentlar soni
    page_size_query_param = 'page_size'  # Foydalanuvchi sahifa hajmini o‘zgartira olishi uchun parametr
    max_page_size = 100  # Maksimal ruxsat etilgan sahifa hajmi
