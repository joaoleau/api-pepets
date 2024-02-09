from rest_framework import serializers
from accounts.api.serializers import AccountSerializer
from .models import Post, Local, Pet
from django.urls import reverse
from django.conf import settings


class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = "__all__"


class PetListSerializer(serializers.ModelSerializer):
    last_local = LocalSerializer()
    owner = serializers.StringRelatedField(many=False)

    class Meta:
        model = Pet
        fields = ["owner", "last_local", "name", "image", "status"]


class PetDetailSerializer(serializers.ModelSerializer):
    last_local = LocalSerializer()
    owner = AccountSerializer()

    class Meta:
        model = Pet
        fields = "__all__"
        read_only_fields = ("owner",)


class PetCreateSerializer(serializers.ModelSerializer):
    last_local = LocalSerializer()

    class Meta:
        model = Pet
        fields = "__all__"


class PostListSerializer(serializers.ModelSerializer):
    pet = PetListSerializer()

    class Meta:
        model = Post
        exclude = ["updated_at", "slug"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["object_url"] = self.generate_url_post_detail(slug=instance.slug)
        return data

    def generate_url_post_detail(self, slug):
        return f"{settings.MY_HOST}{reverse(viewname='posts:rest_posts_detail', kwargs={'slug':slug})}"


class PostDetailSerializer(serializers.ModelSerializer):
    pet = PetDetailSerializer()

    class Meta:
        model = Post
        exclude = ["id", "created_at", "updated_at"]

    def update(self, instance, validated_data):
        pet = validated_data.pop("pet", None)
        if pet:
            local = pet.pop("last_local", None)

            if local:
                for attr, value in local.items():
                    setattr(instance.pet.last_local, attr, value)
                instance.pet.last_local.save()

            for attr, value in pet.items():
                setattr(instance.pet, attr, value)
            instance.pet.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class PostCreateSerializer(serializers.ModelSerializer):
    pet = PetCreateSerializer()

    class Meta:
        model = Post
        exclude = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        pet = validated_data.pop("pet")
        local = pet.pop("last_local")
        local = Local.objects.create(**local)
        pet = Pet.objects.create(last_local=local, **pet)
        instance = self.Meta.model.objects.create(pet=pet, **validated_data)
        return instance
