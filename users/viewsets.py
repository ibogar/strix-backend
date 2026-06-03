from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import ( AllowAny, IsAuthenticated )
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from users.serializers import UserSerializer, LoggedUserSerializer
from .permissions import IsOwner


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

        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwner]

        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def logged_user(self, request):
        serializer = LoggedUserSerializer(request.user)
        return Response(serializer.data)
