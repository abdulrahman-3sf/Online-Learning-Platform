from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class UserRegisterationSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True) # show this only when creating/updating, dont show it when reading

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords must match!'})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')

        user = CustomUser(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            role = validated_data['role']
        )

        user.set_password(validated_data['password']) # will hash the password
        user.save()

        return user
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])

        if user is None:
            raise serializers.ValidationError('Invalid credentials')
        
        data['user'] = user
        return data