from django.db import models


class PetStatusChoices(models.TextChoices):
    LOST = "Lost", "lost"
    FOUND = "Found", "found"


class PetGenderChoices(models.TextChoices):
    FEMALE = "Female", "female"
    MALE = "Male", "male"
    UNKNOWN = "Unknown", "unknown"
