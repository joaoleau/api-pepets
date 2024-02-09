# Generated by Django 5.0.1 on 2024-02-09 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0006_alter_pet_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pet",
            name="type",
            field=models.CharField(
                blank=True,
                choices=[("Dog", "dog"), ("Cat", "cat"), ("Bird", "bird")],
                max_length=5,
                null=True,
                verbose_name="Tipo do Pet",
            ),
        ),
    ]