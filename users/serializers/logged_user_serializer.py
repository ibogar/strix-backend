from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from users.models import User



class LoggedUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
        ]