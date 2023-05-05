from rest_framework.viewsets import ModelViewSet

from authentication.serializers import UserSerializer
from authentication.models import User


class UserAdminViewset(ModelViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
