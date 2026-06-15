from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated, BasePermission)

from .models import Post
from posts.serializers import (PostSerializer, CommentSerializer)



class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        return obj.user == request.user

class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer

    http_method_names = ['get', 'post', 'delete']

    def get_permissions(self):

        if self.action == 'destroy':
            permission_classes = [IsOwner]

        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Post.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):

        post = self.get_object()

        post.likes.add(request.user)

        return Response({
            'likes_count': post.likes.count(),
            'is_liked': True,
        })
    
    @action(detail=True, methods=['delete'])
    def unlike(self, request, pk=None):

        post = self.get_object()

        post.likes.remove(request.user)

        return Response({
            'likes_count': post.likes.count(),
            'is_liked': False,
        })
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):

        post = self.get_object()

        serializer = CommentSerializer(
            post.comments.all(),
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):

        post = self.get_object()

        serializer = CommentSerializer(
            data=request.data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)

        serializer.save(
            user=request.user,
            post=post
        )

        return Response(serializer.data, status=201)