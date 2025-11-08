from rest_framework import serializers
from .models import CustomUser, UserProfile, Category, Course, CourseModule, Lesson
from django.contrib.auth import authenticate

class UserRegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True) # show this only when creating/updating, dont show it when reading

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError({'password': 'Passwords must be at least 8 characters long!'})
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords must match!'})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')

        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password) # will hash the password
        user.save()

        return user
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])

        if user is None:
            raise serializers.ValidationError('Invalid credentials')
        
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled')

        data['user'] = user
        return data
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'date_of_birth', 'expertise']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 
                  'role', 'bio', 'profile_picture', 'profile', 'date_joined']
        read_only_fields = ['id', 'email', 'date_joined']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        # read_only_fields = ['id', 'name', 'slug', 'description']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        exclude = ['module']

class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = CourseModule
        fields = ['id', 'title', 'description', 'order', 'lessons']