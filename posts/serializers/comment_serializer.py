from rest_framework import serializers

from posts.models import Comment


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'content',
        ]

    def get_author(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'full_name': obj.user.full_name,
            'profile_picture': (
                obj.user.profile_picture.url
                if obj.user.profile_picture
                else None
            ),
        }