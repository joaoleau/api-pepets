# Generated by Django 5.0.1 on 2024-02-14 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0010_remove_pet_image_post_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="postsImages/%Y/%m/%d/",
                verbose_name="Image",
            ),
        ),
    ]
