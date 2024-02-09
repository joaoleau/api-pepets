# Generated by Django 5.0.1 on 2024-02-09 19:34

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0012_alter_user__code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="_code",
            field=models.UUIDField(
                default=uuid.UUID("fc25de22-2092-47b5-87c8-b3d9da157e8f"),
                editable=False,
            ),
        ),
    ]
