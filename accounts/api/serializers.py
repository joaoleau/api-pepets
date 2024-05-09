from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.validators import name_validator, password_validator

User = get_user_model()


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone")


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "id")
        read_only_fields = ("first_name", "last_name", "email", "phone", "id")


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        validators=[password_validator],
    )
    re_new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        validators=[password_validator],
    )


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True, style={"input_type": "email"})


class RegisterSerializer(serializers.Serializer):
    username = None
    first_name = serializers.CharField(
        max_length=100, required=True, validators=[name_validator]
    )
    last_name = serializers.CharField(
        max_length=100, required=True, validators=[name_validator]
    )
    email = serializers.EmailField(max_length=100, required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        validators=[password_validator],
    )
    re_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}, required=True
    )

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data.pop("email")
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        validated_data.pop("re_password")
        user = User.objects.create_user(
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            **validated_data,
        )
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        password = validated_data.get("password")
        if password:
            instance.set_password(password)

        instance.save()
        return instance

    def save(self, **kwargs):
        validated_data = {**self.validated_data, **kwargs}

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
            assert (
                self.instance is not None
            ), "`update()` did not return an object instance."
        else:
            self.instance = self.create(validated_data)
            assert (
                self.instance is not None
            ), "`create()` did not return an object instance."

        return self.instance


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        return token


class UserAdminListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)
