from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from users.models import User



class LoggedUserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = [
            'email',
            'full_name',
            'username',
            'bio',
            'profile_picture',
            'password',
            'following',
            'followers'
        ]