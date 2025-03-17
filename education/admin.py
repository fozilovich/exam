from django.contrib import admin
from education.models import Student, Teacher

admin.site.register([Student, Teacher])