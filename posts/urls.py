from django.urls import path
from .views import PostDetailView, PostListView, PostsCreateView

app_name = "posts"

urlpatterns = [
    path("list/", PostListView.as_view(), name="rest_posts_list"),
    path("detail/<int:pk>", PostDetailView.as_view(), name="rest_post_detail"),
    path("create/", PostsCreateView.as_view(), name="rest_post_create"),
]
