from rest_framework import serializers
from accounts.api.serializers import AccountSerializer
from posts.models import Local, Pet
from posts.utils import cleaned_data


class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local
        exclude = (
            "pet",
            "id",
        )

    def validate(self, attrs):
        for field, value in attrs.items():
            attrs[field] = cleaned_data(value)
        return super().validate(attrs)


class PetListSerializer(serializers.ModelSerializer):
    owner = AccountSerializer(read_only=True)
    lastlocal = LocalSerializer(source="local", read_only=True)
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Pet
        fields = "__all__"
        read_only_fields = ["updated_at", "created_at", "slug", "id"]

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        if request is not None:
            return request.build_absolute_uri(obj.get_absolute_url())


class PetDetailSerializer(serializers.ModelSerializer):
    owner = AccountSerializer(read_only=True)
    lastlocal = LocalSerializer(source="local", read_only=True)

    class Meta:
        model = Pet
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "slug"]

    def update_image(self, instance, new_image):
        if instance.image:
            instance.remove_image()
        instance.image = new_image
        instance.save()

    def validate(self, attrs):
        for field, value in attrs.items():
            attrs[field] = cleaned_data(value)
        return super().validate(attrs)


class PetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ["name", "description", "gender", "type", "breed", "reward", "image"]
