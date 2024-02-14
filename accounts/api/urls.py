from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    PasswordResetConfirmView,
    EmailVerifyView,
    PasswordResetView,
    TokenVerifyView,
    TokenRefreshView,
    UserDetailView,
    UsersListView,
    UserMeView,
)

# Rotas Usuário
urlpatterns = [
    path("register/", RegisterView.as_view(), name="rest_user_register"),
    path("verify/<uuid:uuid>/", EmailVerifyView.as_view(), name="rest_user_verify"),
    path("me/", UserMeView.as_view(), name="rest_user_me"),
    path(
        "reset/password/",
        PasswordResetView.as_view(),
        name="rest_email_reset_password",
    ),
    path(
        "reset/password/confirm/<uuid:uuid>/",
        PasswordResetConfirmView.as_view(),
        name="rest_reset_password",
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
    path("admin-api/users/", UsersListView.as_view(), name="rest_users_list"),
    path(
        "admin-api/users/<str:slug>/",
        UserDetailView.as_view(),
        name="rest_user_detail",
    ),
]
