from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    PasswordResetView,
    PasswordResetConfirmView,
    EmailVerifyView,
    TokenVerifyView,
    TokenRefreshView,
    UserDetailView,
    UsersListView,
    UserMeView,
)

# Rotas Usuário
urlpatterns = [
    path("register/", RegisterView.as_view(), name="rest_user_register"),
    path(
        "email/verification/<str:uidb64>/<str:token>/",
        EmailVerifyView.as_view(),
        name="rest_email_verification",
    ),
    path("me/", UserMeView.as_view(), name="rest_user_me"),
    path(
        "reset/password/",
        PasswordResetView.as_view(),
        name="rest_email_reset_password",
    ),
    path(
        "reset/password/confirm/<str:uidb64>/<str:token>/",
        PasswordResetConfirmView.as_view(),
        name="rest_password_reset_confirm",
    ),
]

# Rotas SimpleJWT
urlpatterns += [
    path("login/", LoginView.as_view(), name="rest_login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="rest_token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="rest_token_verify"),
]

# Rotas Administrativas
urlpatterns += [
    path("admin/users/", UsersListView.as_view(), name="rest_users_list"),
    path(
        "admin/users/<int:pk>/",
        UserDetailView.as_view(),
        name="rest_user_detail",
    ),
]
