from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    register_view, 
    login_view, 
    profile_view,
    CategoryViewSet,
    CourseViewSet,
    ModuleViewSet,
    LessonViewSet
)

router = DefaultRouter()

router.register('categories', CategoryViewSet, basename='category')
router.register('courses', CourseViewSet, basename='course')
router.register('modules', ModuleViewSet, basename='module')
router.register('lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    path('auth/register/', register_view, name='register'),
    path('auth/login/', login_view, name='login'),
    path('auth/profile/', profile_view, name='profile'),
    path('', include(router.urls)),
]