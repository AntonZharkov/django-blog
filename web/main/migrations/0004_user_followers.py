# Generated by Django 4.2.2 on 2023-07-26 15:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("actions", "0004_follower"),
        ("main", "0003_user_avatar_user_birthday_user_gender"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="followers",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="writers",
                through="actions.Follower",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
