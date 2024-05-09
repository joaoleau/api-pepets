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
    lastlocal = LocalSerializer(source="local", read_only=True)
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Pet
        fields = ("name", "created_at", "reward", "image", "lastlocal", "absolute_url")

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

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == "image":
                instance.remove_image()
            setattr(instance, attr, value)

        instance.save()

        return instance

    def validate(self, attrs):
        for field, value in attrs.items():
            attrs[field] = cleaned_data(value)
        return super().validate(attrs)

    def validate_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("The name must contain only letters.")
        return value


class PetCreateSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Pet
        fields = [
            "name",
            "description",
            "gender",
            "type",
            "breed",
            "reward",
            "image",
            "status",
            "slug",
            "created_at",
            "updated_at",
            "absolute_url",
        ]
        extra_kwargs = {
            "image": {"required": False},
        }
        read_only_fields = ["id", "created_at", "updated_at", "slug"]

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        if request is not None:
            return request.build_absolute_uri(obj.get_absolute_url())

    def validate_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("The name must contain only letters.")
        return value
