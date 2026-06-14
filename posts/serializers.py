from rest_framework import serializers

from .models import Post

class PostSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'content',
        ]

        read_only_fields = ['user']

    def get_author(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'full_name': obj.user.full_name,
            'profile_picture': (
                obj.user.profile_picture.url
                if obj.user.profile_picture
                else None
            )
        }