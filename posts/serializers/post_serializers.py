from rest_framework import serializers

from posts.models import Post

class PostSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'content',
            'likes_count',
            'is_liked',
            'comment_count',
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
    
    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')

        if request.user.is_anonymous:
            return False

        return obj.likes.filter(id=request.user.id).exists()
    
    def get_comment_count(self, obj):
        return obj.comments.count()