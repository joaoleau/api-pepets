from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.conf import settings
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from .serializers import (
    RegisterSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    LoginSerializer,
    UserMeSerializer,
    UserAdminListSerializer
)
from ..validators import equal_password_and_re_password_validator

User = get_user_model().objects.all()


class RefreshTokenView(TokenRefreshView):
    pass


class VerifyTokenView(TokenVerifyView):
    pass


class UserMeView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserMeSerializer

    def get_queryset(self):
        return get_user_model().objects.filter(id=self.request.user.id)

    def get_object(self):
        return self.get_queryset().first()


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        data = serializer.validated_data
        return Response(data, status=status.HTTP_200_OK)


class UserDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserAdminListSerializer
    queryset = User
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "slug"


class UsersListView(ListAPIView):
    serializer_class = UserAdminListSerializer
    queryset = User
    permission_classes = [permissions.IsAdminUser]


class PasswordResetConfirmView(CreateAPIView):
    serializer_class = PasswordResetConfirmSerializer
    queryset = User

    def get_object(self):
        code = self.kwargs["uuid"]
        obj = get_object_or_404(self.queryset, _code=code)
        return obj

    def post(self, request, *args, **kwargs):
        password = request.data.get("new_password", None)
        re_password = request.data.get("re_new_password", None)

        equal_password_and_re_password_validator(password, re_password)

        instance = self.get_object()
        instance.set_password(password)
        instance.save()

        home = f"{settings.MY_HOST}{reverse(viewname='posts:rest_posts_list')}"
        data = {"links": {"ref": "home", "href": home}}

        return Response(data=data, status=status.HTTP_200_OK)


class PasswordResetView(CreateAPIView):
    serializer_class = PasswordResetSerializer
    queryset = User

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(klass=self.queryset, email=request.data["email"])

        self.send_email_reset_password(user)
        return Response(status=status.HTTP_202_ACCEPTED)

    def send_email_reset_password(self, user):
        subject = "Email for password reset"
        user.email_user(subject=subject, viewname="rest_reset_password")


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        self.send_verification_code(user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def send_verification_code(self, user):
        subject = "Email for account verification"
        user.email_user(subject=subject, viewname="rest_user_verify")

    def perform_create(self, serializer):
        return serializer.save()


class EmailVerifyView(APIView):
    queryset = User
    serializer_class = None

    def get(self, request, *args, **kwargs):

        user = get_object_or_404(klass=self.queryset, _code=self.kwargs["uuid"])

        user.is_active = True
        user.save()
        return Response(status=status.HTTP_202_ACCEPTED)
