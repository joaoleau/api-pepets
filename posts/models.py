from django.db import models
from accounts.models import User
from .choices import PetGenderChoices, PetStatusChoices
from .managers import PostManager
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from PIL import Image
import string
import posixpath
import random
import uuid
import os


class ImageField(models.ImageField):
    def generate_filename(self, instance, filename):
        if callable(self.upload_to):
            filename = self.upload_to(instance, filename)
        else:
            file_extension = filename.split(".")[-1].lower()
            filename = f"{uuid.uuid4().hex}.{file_extension}"
            dirname = str(self.upload_to)
            filename = posixpath.join(dirname, filename)
        return self.storage.generate_filename(filename)


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
        OTHERS = "Others", "others"

    name = models.CharField(max_length=10, verbose_name=_("Pet Name"))
    description = models.CharField(max_length=280, verbose_name=_("Pet Description"))
    type = models.CharField(
        max_length=6, choices=PetType.choices, verbose_name=_("Pet Type")
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
        verbose_name=_("Last Location"),
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("Owner"), related_name="pet"
    )

    def __str__(self) -> str:
        return f"{self.name}, 'last_local':{self.last_local}"


class Post(BaseModel):
    description = models.CharField(max_length=280, verbose_name=_("Description"))
    title = models.CharField(max_length=50, verbose_name=_("Title"))
    is_published = models.BooleanField(default=True)
    image = ImageField(upload_to="posts-images/", verbose_name=_("Image"), default="")
    reward = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Reward"),
    )
    slug = models.SlugField(max_length=100, blank=True, null=True)
    pet = models.OneToOneField(Pet, on_delete=models.CASCADE, related_name="post")

    objects = PostManager()

    def image_path(self):
        return os.path.join(settings.MEDIA_ROOT, self.image.name)

    def remove_image(self):
        if self.image:
            image_path = self.image_path()
            if os.path.exists(image_path):
                os.remove(image_path)
            self.image = None
            self.save()

    def resize_image(self, new_width=800):
        img_full_path = self.image_path()
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size

        if original_width <= new_width:
            img_pil.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(img_full_path, optimize=True, quality=50)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f'{self.pet.name}{"".join(random.choice(string.digits) for _ in range(4))}'
            )

        super().save(*args, **kwargs)

        max_image_size = 1200
        if self.image:
            self.resize_image(max_image_size)

    def delete(self, using=None, keep_parents=False):
        self.remove_image()
        return super().delete(using, keep_parents)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self) -> str:
        return f"{self.title}, {self.pet}"
