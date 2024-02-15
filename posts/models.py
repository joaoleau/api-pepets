from django.db import models
from accounts.models import User
from .choices import PetGenderChoices, PetStatusChoices
from .managers import PostManager
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
import string
import random


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Local(models.Model):
    street = models.CharField(max_length=100, verbose_name=_("Street"))
    neighborhood = models.CharField(max_length=100, verbose_name=_("Neighborhood"))
    city = models.CharField(max_length=100, verbose_name=_("City"))

    def __str__(self) -> str:
        return f"{self.street}, {self.neighborhood}, {self.city}"


class Pet(models.Model):
    class PetType(models.TextChoices):
        DOG = "Dog", "dog"
        CAT = "Cat", "cat"
        BIRD = "Bird", "bird"

    name = models.CharField(max_length=10, verbose_name=_("Pet Name"))
    description = models.CharField(max_length=280, verbose_name=_("Pet Description"))
    type = models.CharField(
        max_length=5, choices=PetType.choices, verbose_name=_("Pet Type")
    )
    gender = models.CharField(
        max_length=7, choices=PetGenderChoices.choices, verbose_name=_("Gender")
    )
    breed = models.CharField(max_length=50, verbose_name=_("Breed"))
    status = models.CharField(
        max_length=6, choices=PetStatusChoices.choices, verbose_name=_("Status")
    )
    last_local = models.ForeignKey(
        Local,
        on_delete=models.SET_NULL,
        related_name="pets",
        null=True,
        blank=True,
        verbose_name="Last Location",
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Owner"))

    def __str__(self) -> str:
        return f"{self.name}, 'last_local':{self.last_local}"


class Post(BaseModel):
    description = models.CharField(max_length=280, verbose_name=_("Description"))
    title = models.CharField(max_length=50, verbose_name=_("Title"))
    is_published = models.BooleanField(default=True)
    image = models.ImageField(
        upload_to="postsImages/%Y/%m/%d/", verbose_name=_("Image"), default=""
    )
    reward = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Reward"),
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

    def __str__(self) -> str:
        return f"{self.title}, {self.pet}"
