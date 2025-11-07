from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, Category, Course, CourseModule, Lesson


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

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(CourseModule)
admin.site.register(Lesson)