# Generated by Django 5.0.1 on 2024-02-13 19:31

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0008_remove_user_email_validated_alter_user_is_active"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="role",
        ),
        migrations.AlterField(
            model_name="user",
            name="_code",
            field=models.UUIDField(
                default=uuid.UUID("f4286b2a-b56a-49f9-9a39-5972e49b65d0"),
                editable=False,
            ),
        ),
    ]