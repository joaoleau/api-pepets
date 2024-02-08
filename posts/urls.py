from django.urls import path
from .views import (
    PostDetailView,
    PostListView,
    PostCreateView,
    PostMeView,
    PostUserListView,
    PostFilterListView,
)

app_name = "posts"

urlpatterns = [
    path("posts/", PostListView.as_view(), name="rest_posts_list"),
    path("posts/<str:slug>", PostDetailView.as_view(), name="rest_posts_detail"),
    path("posts/<str:status>/", PostFilterListView.as_view(), name="rest_posts_status"),
    path("me/posts/create/", PostCreateView.as_view(), name="rest_posts_create"),
    path("me/posts/", PostMeView.as_view(), name="rest_posts_me"),
]

urlpatterns += [
    path("<str:slug>/posts/", PostUserListView.as_view(), name="rest_user_posts"),
]
