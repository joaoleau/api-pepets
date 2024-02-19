from django.urls import path
from .views import (
    PostDetailView,
    PostListView,
    PostCreateView,
    PostMeView,
    PostUserListView,
    CommentsView
)

app_name = "posts"

urlpatterns = [
    path("posts/<str:slug>/", PostDetailView.as_view(), name="rest_posts_detail"),
    path("posts/", PostListView.as_view(), name="rest_posts_list"),
    path("me/posts/create/", PostCreateView.as_view(), name="rest_posts_create"),
    path("me/posts/", PostMeView.as_view(), name="rest_posts_me"),
    path("comments/<pk:pk>/", CommentsView.as_view(), name="posts:rest_comments_detail")
]

urlpatterns += [
    path("<str:slug>/posts/", PostUserListView.as_view(), name="rest_user_posts"),
]
