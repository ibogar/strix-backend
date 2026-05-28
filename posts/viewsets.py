from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer

class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all()

    @action(detail=False, methods=['get'])
    def feed(self, request):

        posts = Post.objects.filter(
            user__in=request.user.following.all()
        ).order_by('-created_at')

        serializer = self.get_serializer(posts, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def mine(self, request):

        posts = Post.objects.filter(
            user=request.user
        ).order_by('-created_at')

        serializer = self.get_serializer(posts, many=True)

        return Response(serializer.data)