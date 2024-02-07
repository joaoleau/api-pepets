from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .permissions import IsAuthorOrIsAuthenticatedReadOnly
from rest_framework.permissions import (
    IsAuthenticated,
)
from .models import Post
from .serializers import PostListSerializer, PostCreateSerializer, PostDetailSerializer
from rest_framework.response import Response
from rest_framework import status


PostQuerySet = Post.objects.published()


class AccountPostsListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostListSerializer

    def get_queryset(self):
        return Post.objects.filter(author__slug=self.kwargs["slug"])


class PostsCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostCreateSerializer
    queryset = PostQuerySet

    def post(self, request, *args, **kwargs):
        request.data["pet"]["owner"] = request.user.id
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class PostDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrIsAuthenticatedReadOnly]
    serializer_class = PostDetailSerializer
    queryset = PostQuerySet
    lookup_field = "slug"


class PostListView(ListAPIView):
    serializer_class = PostListSerializer
    queryset = PostQuerySet
