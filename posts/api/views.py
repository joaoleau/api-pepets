from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .permissions import IsAuthorOrIsAuthenticatedReadOnly
from rest_framework.permissions import (
    IsAuthenticated,
)
from ..models import Post
from .serializers import PostListSerializer, PostCreateSerializer, PostDetailSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework import pagination
from django_filters.rest_framework import DjangoFilterBackend


PostQuerySet = Post.objects.published()


class PostPagination(pagination.PageNumberPagination):
    page_size = 25


class PostUserListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostListSerializer
    queryset = Post.objects.published()

    def get_queryset(self):
        return self.queryset.filter(pet__owner__slug=self.kwargs.get("slug"))

    def get(self, request, slug, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PostMeView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostListSerializer
    queryset = Post.objects.published()

    def get_queryset(self):
        return Post.objects.filter(pet__owner__slug=self.request.user.slug)


class PostCreateView(CreateAPIView):
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
    pagination_class = PostPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "pet__status",
        "pet__type",
        "pet__last_local__street",
        "pet__last_local__neighborhood",
        "pet__last_local__city",
    ]
    search_fields = [
        "pet__description",
        "description",
        "title",
    ]
    ordering_fields = ["created_at"]

    def paginate_queryset(self, queryset):
        return super().paginate_queryset(queryset)
