from rest_framework import serializers
from accounts.api.serializers import AccountSerializer
from .models import Post
from .utils import generate_link_post_detail


class PostsModelSerializer(serializers.ModelSerializer):
    author = AccountSerializer()

    class Meta:
        model = Post
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["object_link"] = generate_link_post_detail(post_id=instance.pk)
        return data
    

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # fields = "__all__"
        exclude = ["id", "created_at", "updated_at"]

