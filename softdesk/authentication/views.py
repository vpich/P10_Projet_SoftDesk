from rest_framework.generics import CreateAPIView

from authentication.serializers import CreateUserSerializer
from authentication.models import User


class SignupView(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
