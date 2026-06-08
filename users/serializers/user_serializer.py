from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from users.models import User



class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    email = serializers.CharField(write_only=True, required=True)
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'full_name',
            'username',
            'password',
            'bio',
            'profile_picture',
            'following_count',
            'followers_count',
        ]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user