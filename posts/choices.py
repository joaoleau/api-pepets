from django.db import models


class PostStatusChoices(models.TextChoices):
    LOST = "Lost", "lost"
    FOUND = "Found", "found"


class PostGenreChoices(models.TextChoices):
    FEMALE = "Female", "female"
    MALE = "Male", "male"
