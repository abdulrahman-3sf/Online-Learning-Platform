from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, Category, Course, CourseModule, Lesson, Enrollment


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

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'progress_percentage', 'is_completed', 'enrolled_at']
    list_filter = ['is_completed', 'enrolled_at']
    search_fields = ['student__email', 'course__title']
    readonly_fields = ['enrolled_at', 'completed_at']