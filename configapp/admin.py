from django.contrib import admin
from configapp.models import User, Course, Group

admin.site.register([User, Course, Group])
