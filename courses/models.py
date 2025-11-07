from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('INSTRUCTOR', 'Instructor'),
        ('ADMIN', 'Admin')
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STUDENT')
    bio = models.TextField(blank=True, null=True, help_text='Short bio about yourself')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, help_text='Profile picture')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email
    
    def get_fullname(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True)
    data_of_birth = models.DateField(blank=True, null=True)
    expertise = models.TextField(blank=True, help_text='Areas of expertise (for instructors)')

    def __str__(self):
        return f'{self.user.get_fullname()}\'s Profile'
    
    class Meta:
        db_table = 'profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Course(models.Model):
    LEVEL_CHOICES = (
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced')
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='courses/thumbnails/', blank=True, null=True)

    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='courses')

    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='BEGINNER')
    duration = models.IntegerField(blank=True, null=True, help_text='Duration in minutes')
    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.title
    
class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']
        unique_together = ['course', 'order']
        verbose_name = 'Course Module'
        verbose_name_plural = 'Course Modules'

    def __str__(self):
        return f'{self.course.title} - {self.title}'
    
class Lesson(models.Model):
    LESSON_TYPE_CHOICES = (
        ('VIDEO', 'Video'),
        ('ARTICLE', 'Article'),
        ('DOCUMENT', 'Document')
    )

    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True, help_text='Text content for article lessons')
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE_CHOICES, default='VIDEO')
    order = models.IntegerField()
    
    video_url = models.URLField(blank=True, null=True, help_text='YouTube or Vimeo URL')
    document_file = models.FileField(upload_to='lessons/documents/',blank=True, null=True, help_text='PDF, DOCX, etc.')

    duration = models.IntegerField(blank=True, null=True, help_text='Duration in minutes')
    is_preview = models.BooleanField(default=False, help_text='Can non-enrolled students view this lesson?')

    class Meta:
        ordering = ['order']
        unique_together = ['module', 'order']
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'

    def __str__(self):
        return f'{self.module.title} - {self.title}'