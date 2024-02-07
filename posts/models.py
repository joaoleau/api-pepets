from django.db import models
from accounts.models import User
from .choices import PetGenderChoices, PetStatusChoices
from .managers import PostManager
from django.utils.text import slugify
import string
import random


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Local(models.Model):
    street = models.CharField(max_length=100, verbose_name="Rua")
    neighborhood = models.CharField(max_length=100, verbose_name="Bairro")
    city = models.CharField(max_length=100, verbose_name="Cidade")

    def __str__(self) -> str:
        return self.__dict__()


class Pet(models.Model):
    name = models.CharField(max_length=30, verbose_name="Nome do Pet")
    description = models.CharField(max_length=280, verbose_name="Descrição do Pet")
    gender = models.CharField(
        max_length=7, choices=PetGenderChoices.choices, verbose_name="Gênero"
    )
    breed = models.CharField(max_length=30, verbose_name="Raça")
    status = models.CharField(
        max_length=6, choices=PetStatusChoices.choices, verbose_name="Situação"
    )
    image = models.ImageField(upload_to="posts/", default="", verbose_name="Imagem")
    last_local = models.ForeignKey(
        Local,
        on_delete=models.SET_NULL,
        related_name="pets",
        null=True,
        blank=True,
        verbose_name="Última localização",
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Tutor")

    def __str__(self) -> str:
        return f"{self.name}- {self.description}, 'last_local':{self.last_local}"


class Post(BaseModel):
    description = models.CharField(max_length=280, verbose_name="Descrição")
    title = models.CharField(max_length=30, verbose_name="Titulo")
    is_published = models.BooleanField(default=True)
    reward = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Recompensa",
    )
    slug = models.SlugField(max_length=100, blank=True, null=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    objects = PostManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f'{self.pet.name}{"".join(random.choice(string.digits) for _ in range(4))}'
            )
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
