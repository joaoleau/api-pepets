# Generated by Django 5.0.1 on 2024-02-09 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0004_alter_pet_breed_alter_post_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="pet",
            name="type",
            field=models.CharField(
                choices=[("Dog", "dog"), ("Cat", "cat"), ("Bird", "bird")],
                default="Dog",
                max_length=5,
                verbose_name="Tipo do Pet",
            ),
            preserve_default=False,
        ),
    ]
