# Generated by Django 4.1 on 2024-08-03 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sublets", "0002_listing_message_listingphoto_user_saved_listings"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="zip_code",
            field=models.CharField(default=10000, max_length=5),
            preserve_default=False,
        ),
    ]
