# Generated by Django 4.2.2 on 2023-07-12 10:50

import main.services
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_set_superuser"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                blank=True,
                default="no-image-available.jpg",
                upload_to=main.services.user_directory_path,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="birthday",
            field=models.DateField(blank=True, null=True, verbose_name="Birthday"),
        ),
        migrations.AddField(
            model_name="user",
            name="gender",
            field=models.PositiveSmallIntegerField(
                choices=[(0, "Unknown"), (1, "Man"), (2, "Female")],
                default=0,
                verbose_name="Gender",
            ),
        ),
    ]
