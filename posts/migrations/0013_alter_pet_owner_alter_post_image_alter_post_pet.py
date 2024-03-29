# Generated by Django 5.0.1 on 2024-02-15 23:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0012_alter_post_image"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="pet",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pet",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Owner",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(
                default="", upload_to="posts/%m/%d/", verbose_name="Image"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="pet",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="post",
                to="posts.pet",
            ),
        ),
    ]
