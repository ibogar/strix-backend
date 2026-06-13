from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from users.models import User



class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

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
            'following',
            'following_count',
            'followers',
            'followers_count',
            'is_following',
        ]

    def get_followers(self, obj):
        return [
            {
                'id': user.id,
                'username': user.username,
                'full_name': user.full_name,
                'profile_picture': user.profile_picture.url if user.profile_picture else None,
            }
            for user in obj.followers.all()
        ]

    def get_following(self, obj):
        return [
            {
                'id': user.id,
                'username': user.username,
                'full_name': user.full_name,
                'profile_picture': user.profile_picture.url if user.profile_picture else None,
                'is_following': True,
            }
            for user in obj.following.all()
        ]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()
    
    def get_is_following(self, obj):

        request = self.context.get('request')

        if not request:
            return False

        if request.user.is_anonymous:
            return False

        return request.user.following.filter(
            id=obj.id
        ).exists()

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user