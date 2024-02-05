from django.db import models
from django.db.models.query import QuerySet


class PostQuerySet(models.QuerySet):
    def publish(self):
        return self.update(is_published=True)


class PostManager(models.Manager):
    def published(self):
        return self.filter(is_published=True)

    def get_queryset(self) -> QuerySet:
        return PostQuerySet(self.model, using=self._db)
