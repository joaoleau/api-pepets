from django.urls import path
from posts.views import AccountPostsListView
from .views import (
    RegisterView,
    LoginView,
    PasswordResetConfirmView,
    EmailVerifyView,
    PasswordResetView,
    TokenVerifyView,
    TokenRefreshView,
    AccountsDetailsView,
    AccountsListView,
    AccountMeView,
)


urlpatterns = [
    path("accounts/", AccountsListView.as_view(), name="rest_accounts_list"),
    path(
        "accounts/<str:slug>/",
        AccountsDetailsView.as_view(),
        name="rest_account_detail",
    ),
    path("me/", AccountMeView.as_view(), name="rest_account_me_detail"),
]


urlpatterns += [
    path("verify/<uuid:uuid>/", EmailVerifyView.as_view(), name="rest_account_verify"),
    path("register/", RegisterView.as_view(), name="rest_account_register"),
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


urlpatterns += [
    path("login/", LoginView.as_view(), name="rest_login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="rest_token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="rest_token_verify"),
]


urlpatterns += [
    path(
        "<str:slug>/posts/", AccountPostsListView.as_view(), name="rest_account_posts"
    ),
]
