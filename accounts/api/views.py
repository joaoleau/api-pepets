from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.conf import settings
from .serializers import (
    RegisterSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    LoginSerializer,
    AccountSerializer,
    AccountsListSerializer,
)
from django.urls import reverse
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from ..utils import send_code
from .permissions import IsOwnerOrAdminOrReadOnlyPermission
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from posts.models import Post
from posts.serializers import PostListSerializer

User = get_user_model().objects.all()


class RefreshTokenView(TokenRefreshView):
    pass


class VerifyTokenView(TokenVerifyView):
    pass


class AccountMeView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostListSerializer

    def get_queryset(self):
        return Post.objects.filter(pet__owner__id=self.request.user.id)


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


class AccountsDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer
    queryset = User
    permission_classes = [IsOwnerOrAdminOrReadOnlyPermission]
    lookup_field = "slug"


class AccountsListView(ListAPIView):
    serializer_class = AccountsListSerializer
    queryset = User
    permission_classes = [permissions.IsAdminUser]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PasswordResetConfirmView(CreateAPIView):
    serializer_class = PasswordResetConfirmSerializer
    queryset = User

    def get_object(self):
        obj = get_object_or_404(self.queryset, **self.kwargs)
        return obj

    def post(self, request, *args, **kwargs):
        password = request.data.pop("new_password", None)
        re_password = request.data.pop("re_new_password", None)

        if (password or re_password) is None:
            data = {"error": "new_password não foi inserida"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if password != re_password:
            data = {"error": "new_password e re_new_password são diferentes"}

            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()
        instance.set_password(password)
        instance.save()

        url = f"{settings.MY_HOST}{reverse(viewname='posts:rest_posts_list')}"
        data = {"links": {"ref": "home - posts list", "href": url}}

        return Response(data=data, status=status.HTTP_200_OK)


class PasswordResetView(CreateAPIView):
    serializer_class = PasswordResetSerializer
    queryset = User

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(
            klass=self.queryset, email=request.data["email"])
        subject = "Email para redefinição de senha"
        url = f"{settings.MY_HOST}{reverse(viewname='rest_reset_password', kwargs={'slug':user.slug, 'code':user.code})}"
        message = f"Link para redefinição de senha: {url}"
        send_code(subject=subject, message=message, email=user.email)
        data = request.data
        data["links"] = {"ref": "redefinição de senha", "href": url}
        return Response(data=data, status=status.HTTP_202_ACCEPTED)


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        self.send_verification_code(request)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def send_verification_code(self, request):
        user = get_object_or_404(self.queryset, email=request.data["email"])
        subject = "Email para verificação da conta"
        verify_link = f"{settings.MY_HOST}{reverse(viewname='rest_account_verify', kwargs={'uuid':user.code})}"
        send_code(subject=subject, message=verify_link, email=user.email)

    def perform_create(self, serializer):
        serializer.save()


class EmailVerifyView(APIView):
    queryset = User

    def get(self, request, *args, **kwargs):

        user = get_object_or_404(
            klass=self.queryset, _code=self.kwargs["uuid"])

        user.email_validated = True
        user.save()
        return Response(status=status.HTTP_202_ACCEPTED)
