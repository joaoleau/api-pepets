# Generated by Django 5.0.1 on 2024-02-05 21:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("pet_description", models.CharField(max_length=280)),
                ("pet_name", models.CharField(max_length=30)),
                (
                    "pet_genre",
                    models.CharField(
                        choices=[("Female", "female"), ("Male", "male")], max_length=6
                    ),
                ),
                ("pet_breed", models.CharField(max_length=30)),
                ("status", models.CharField(default="Lost", max_length=6)),
                ("is_published", models.BooleanField(default=True)),
                ("pet_images", models.ImageField(default="", upload_to="posts/")),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Post",
                "verbose_name_plural": "Posts",
            },
        ),
    ]
