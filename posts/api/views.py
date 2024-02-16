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


class PostPagination(pagination.PageNumberPagination):
    page_size = 25


class PostUserListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostListSerializer
    queryset = Post.objects.published()

    def get_queryset(self):
        qs = self.queryset.filter(pet__owner__slug=self.kwargs.get("slug"))
        qs = qs.select_related("pet__last_local", "pet__owner")
        return qs

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
    queryset = Post.objects.published()

    def post(self, request, *args, **kwargs):

        if request.user.is_staff and request.data["pet"].get("owner", None) is not None:
            return self.create(request, *args, **kwargs)
        request.data["pet"].update({"owner": request.user.id})
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
    queryset = Post.objects.published()
    lookup_field = "slug"

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)
        return Response(serializer.data)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class PostListView(ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post
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

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.objects.published()
        qs = qs.select_related("pet", "pet__last_local", "pet__owner")
        return qs
