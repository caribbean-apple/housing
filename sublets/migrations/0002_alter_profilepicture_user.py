# Generated by Django 4.1 on 2024-08-06 04:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("sublets", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profilepicture",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="profile_pictures",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
