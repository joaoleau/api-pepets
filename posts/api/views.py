from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import mixins
from .permissions import IsAuthorOrIsAuthenticatedReadOnly, IsAuthorObject
from rest_framework.permissions import (
    IsAuthenticated,
)
from posts.models import Pet, Local
from .serializers import (
    PetListSerializer,
    PetCreateSerializer,
    PetDetailSerializer,
    LocalSerializer,
)
from rest_framework import filters
from rest_framework import pagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404


class PostPagination(pagination.PageNumberPagination):
    page_size = 25


class MePetsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PetListSerializer

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user)


class PetCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PetCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PetDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrIsAuthenticatedReadOnly]
    serializer_class = PetDetailSerializer
    queryset = Pet.objects.all()
    lookup_field = "slug"


class PetListView(ListAPIView):
    serializer_class = PetListSerializer
    queryset = Pet.objects.published()
    pagination_class = PostPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "status",
        "type",
        "local__street",
        "local__neighborhood",
        "local__city",
    ]
    search_fields = [
        "description",
    ]
    ordering_fields = ["created_at"]

    def paginate_queryset(self, queryset):
        return super().paginate_queryset(queryset)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("local", "owner")
        return qs


class LastLocalUpdateView(mixins.UpdateModelMixin, GenericAPIView):
    permission_classes = [IsAuthorObject]
    serializer_class = LocalSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        obj = get_object_or_404(Local.objects.all(), pet__slug=self.kwargs.get("slug"))
        self.check_object_permissions(self.request, obj)
        return obj
