from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework import serializers

from authentication.models import User


class CreateUserSerializer(ModelSerializer):

    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label="Confirmez votre mot de passe"
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "password2",
        ]
        extra_kwargs = {
            "password": {"style": {'input_type': 'password'},
                         "write_only": True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise ValidationError(
                {
                    "password": "Les champs de mot de passe "
                                "ne sont pas identiques."
                }
            )
        elif not attrs["first_name"]:
            raise ValidationError(
                {
                    "first_name": "Vous devez "
                                  "saisir un prénom."
                }
            )
        elif not attrs["last_name"]:
            raise ValidationError(
                {
                    "last_name": "Vous devez "
                                 "saisir un nom de famille."
                }
            )
        return attrs

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                email=validated_data["email"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                password=validated_data["password"],
            )
        except ValueError as e:
            raise ValidationError({"champs incorrect": e})

        return user
