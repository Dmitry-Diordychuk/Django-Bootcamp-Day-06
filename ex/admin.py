from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Tip
from django.contrib.auth.models import Permission

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Tip)
admin.site.register(Permission)
