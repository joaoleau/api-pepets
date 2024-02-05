from django.urls import path
from posts.views import AccountPostsListView
from .views import (
    RegisterView,
    LoginView,
    PasswordResetView,
    CodeVerifyView,
    EmailPasswordResetView,
    TokenVerifyView,
    TokenRefreshView,
    AccountsDetailsView,
    AccountsListView,
)


urlpatterns = [
    path("accounts/", AccountsListView.as_view(), name="rest_accounts_list"),
    path("accounts/<str:slug>/", AccountsDetailsView.as_view(), name="rest_account_detail"),
]


urlpatterns += [
    path("verify/", CodeVerifyView.as_view(), name="rest_account_verify"),
    path("register/", RegisterView.as_view(), name="rest_account_register"),
    path(
        "reset/password/",
        EmailPasswordResetView.as_view(),
        name="rest_email_reset_password",
    ),
    path(
        "reset/password/confirm/<str:slug>/<str:code>/",
        PasswordResetView.as_view(),
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
