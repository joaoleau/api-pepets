from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .permissions import IsAuthorOrIsAuthenticatedReadOnly
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from .models import Post
from .serializers import PostsModelSerializer, PostCreateSerializer

PostQuerySet = Post.objects.published()


class AccountPostsListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostsModelSerializer

    def get_queryset(self):
        return Post.objects.filter(author__slug=self.kwargs["slug"])


class PostsCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostCreateSerializer
    queryset = PostQuerySet

    def post(self, request, *args, **kwargs):

        request.data["author"] = request.user.id
        return super().create(request, *args, **kwargs)


class PostDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrIsAuthenticatedReadOnly]
    serializer_class = PostsModelSerializer
    queryset = PostQuerySet

    # lookup_field = 'pk'
    # lookup_url_kwarg = 'pk'

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     data = serializer.data
    #     data["email"] = serializer.link()
    #     return Response(data)

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.get("partial", False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(
    #         instance=instance,
    #         data=request.data,
    #         partial=partial,
    #         many=False,
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     data = serializer.data
    #     data["link"] = serializer.link()
    #     return Response(data)


class PostListView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostsModelSerializer
    queryset = PostQuerySet

    # def get_serializer(self, *args, **kwargs):
    #     return self.serializer_class(*args, **kwargs)

    # def get_serializer_class(self):
    #     return self.serializer_class

    # def list(self, request, *args, **kwargs):

    #     queryset = self.filter_queryset(self.get_queryset())

    #     # page = self.paginate_queryset(queryset)
    #     # if page is not None:
    #     #     serializer = self.get_serializer(page, many=True)
    #     #     return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     value = serializer.link()
    #     print(value)

    # data = serializer.data
    # data["link"] = serializer.link()
    # return Response(data)

    # def get_queryset(self):
    #     if self.request.user.is_staff:
    #         return Post.objects.all()

    #     return self.queryset
