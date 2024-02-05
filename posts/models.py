from django.db import models
from accounts.models import User
from .choices import PostGenreChoices, PostStatusChoices
from .managers import PostManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(BaseModel):
    pet_description = models.CharField(max_length=280)
    pet_name = models.CharField(max_length=30)
    pet_genre = models.CharField(max_length=6, choices=PostGenreChoices.choices)
    pet_breed = models.CharField(max_length=30)
    status = models.CharField(max_length=6, default=PostStatusChoices.LOST)
    is_published = models.BooleanField(default=True)
    pet_images = models.ImageField(upload_to="posts/", default="")
    pet_last_local = None
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = PostManager()

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self) -> str:
        return f"{self.id} - {self.pet_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
