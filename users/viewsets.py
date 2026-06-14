from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import ( AllowAny, IsAuthenticated )
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from .models import User
from users.serializers import UserSerializer, LoggedUserSerializer
from .utils import IsOwner
from posts.serializers import PostSerializer


class UserViewSet(ModelViewSet):

    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer

    lookup_field = 'username'

    filter_backends = [SearchFilter]
    search_fields = [
        'username',
        'full_name',
    ]

    def get_permissions(self):

        if self.action == 'create':
            permission_classes = [AllowAny]

        elif self.action in ['update', 'partial_update', 'destroy', 'logged_user']:
            permission_classes = [IsOwner]

        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def logged_user(self, request):
        serializer = LoggedUserSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def follow(self, request, username=None):

        target_user = self.get_object()

        request.user.following.add(target_user)

        return Response({
            "message": "User followed"
        })

    @action(detail=True, methods=['post'])
    def unfollow(self, request, username=None):

        target_user = self.get_object()

        request.user.following.remove(target_user)

        return Response({
            "message": "User unfollowed"
        })

    @action(detail=True, methods=['get'])
    def posts(self, request, username=None):

        user = self.get_object()

        posts = user.posts.all()

        serializer = PostSerializer(posts, many=True, context=self.get_serializer_context())

        return Response(serializer.data)