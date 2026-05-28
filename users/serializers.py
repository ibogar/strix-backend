from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import User



class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = [
            'email',
            'full_name',
            'username',
            'password',
            'bio',
            'profile_picture',
        ]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user