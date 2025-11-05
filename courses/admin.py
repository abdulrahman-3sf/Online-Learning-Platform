from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'role', 'is_staff']

    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'bio', 'profile_picture')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role', 'bio', 'profile_picture')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)