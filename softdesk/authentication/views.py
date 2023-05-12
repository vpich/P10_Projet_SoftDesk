from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import CreateAPIView

from authentication.serializers import UserSerializer, CreateUserSerializer
from authentication.models import User


class UserAdminViewset(ModelViewSet):

    serializer_class = UserSerializer

    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return User.objects.all()


class SignupView(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
