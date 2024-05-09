from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from accounts.api.token import user_tokenizer_generate
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.db import IntegrityError
from accounts.validators import equal_password_and_re_password_validator_or_400
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from accounts.api.serializers import (
    RegisterSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    LoginSerializer,
    UserMeSerializer,
    UserAdminListSerializer,
)

User = get_user_model()


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.perform_create(serializer)

            self.send_verification_code(user, get_current_site(request))

            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        except IntegrityError:
            return Response(data={"error":"Email address already in use."}, status=status.HTTP_400_BAD_REQUEST) 

    def send_verification_code(self, user, current_site):
        subject = "Activate your account"
        message = render_to_string(
            "email-verification.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": user_tokenizer_generate.make_token(user),
            },
        )
        user.email_user(subject=subject, message=message)

    def perform_create(self, serializer):
        return serializer.save()


class EmailVerifyView(APIView):

    def get(self, request, *args, **kwargs):
        unique_token = force_str(urlsafe_base64_decode(self.kwargs["uidb64"]))
        user = User.objects.get(pk=unique_token)

        if user and user_tokenizer_generate.check_token(user, self.kwargs["token"]):
            user.is_active = True
            user.save()

            return Response(
                data={"data": "Account verified successfully!"},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            data={"error": "Could not verify."}, status=status.HTTP_400_BAD_REQUEST
        )


class PasswordResetConfirmView(CreateAPIView):
    serializer_class = PasswordResetConfirmSerializer
    queryset = User.objects.all()

    def get_object(self):
        token = self.kwargs["unique_token"]
        obj = get_object_or_404(self.queryset, pk=token)
        return obj

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        unique_token = force_str(urlsafe_base64_decode(self.kwargs["uidb64"]))
        self.kwargs["unique_token"] = unique_token
        user = self.get_object()

        if user and user_tokenizer_generate.check_token(user, self.kwargs["token"]):
            password = request.data.get("new_password", None)
            re_password = request.data.get("re_new_password", None)

            equal_password_and_re_password_validator_or_400(password, re_password)

            user.set_password(password)
            user.save()

            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(CreateAPIView):
    serializer_class = PasswordResetSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(klass=self.queryset, email=request.data["email"])

        self.send_email_reset_password(user, get_current_site(request))
        return Response(status=status.HTTP_202_ACCEPTED)

    def send_email_reset_password(self, user, current_site):
        subject = "Reset Password"
        message = render_to_string(
            "email_reset_password.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": user_tokenizer_generate.make_token(user),
            },
        )
        user.email_user(subject=subject, message=message)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class RefreshTokenView(TokenRefreshView):
    pass


class VerifyTokenView(TokenVerifyView):
    pass


class UserMeView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserMeSerializer

    def get_queryset(self):
        return get_user_model().objects.get(id=self.request.user.id)

    def get_object(self):
        return self.get_queryset()


class UserDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserAdminListSerializer
    queryset = User
    permission_classes = [permissions.IsAdminUser]


class UsersListView(ListAPIView):
    serializer_class = UserAdminListSerializer
    queryset = User
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related("groups", "user_permissions")
        return qs
