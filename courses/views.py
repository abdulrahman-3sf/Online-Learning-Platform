from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegisterationSerializer, UserLoginSerializer, UserSerializer, CategorySerializer, CourseListSerializer, CourseDetailSerializer, ModuleSerializer, LessonSerializer
from .models import Category, Course, CourseModule, Lesson
from .permissions import IsInstructorOrReadOnly

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = UserRegisterationSerializer(data=request.data)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': 'Failed to create user', 'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = UserLoginSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        user_serializer = UserSerializer(user)

        response_data = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': user_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    if request.method == 'GET':
        user = request.user

        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method in ['PUT', 'PATCH']:
        is_partial = request.method == 'PATCH'

        user = request.user

        serializer = UserSerializer(user, data=request.data, partial=is_partial)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    permission_classes = [IsInstructorOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and user.role == 'INSTRUCTOR':
            return Course.objects.filter(instructor=user)
        else:
            return Course.objects.filter(is_published=True)
        
    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        elif self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseListSerializer
    
    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = CourseModule.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsInstructorOrReadOnly]

    def get_queryset(self):
        course_id = self.request.query_params.get('course_id')

        if course_id:
            queryset = queryset.filter(course_id=course_id)

        return queryset
    
    def perform_create(self, serializer):
        course_id = self.request.data.get('course')

        if not course_id:
            raise ValueError('Course field is required!')

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise ValueError('Course not found!')

        if course.instructor != self.request.user:
            raise PermissionDenied('You can only add modules to your own courses!')
        
        serializer.save(course=course)

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsInstructorOrReadOnly]

    def get_queryset(self):
        module_id = self.request.query_params.get('module_id')

        if module_id:
            queryset = queryset.filter(id=module_id)

        return queryset
    
    def perform_create(self, serializer):
        module_id = self.request.data.get('module')

        if not module_id:
            raise ValueError('Module field is required!')
        
        try:
            module = CourseModule.objects.get(id=module_id)
        except CourseModule.DoesNotExist:
            raise ValueError('Module not found!')
        
        if module.course.instructor != self.request.user:
            raise PermissionDenied("You can only add lessons to your own courses!")
        
        serializer.save(module=module)