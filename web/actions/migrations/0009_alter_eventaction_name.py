# Generated by Django 4.2.2 on 2023-08-15 14:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("actions", "0008_eventaction"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventaction",
            name="name",
            field=models.CharField(
                choices=[
                    ("update_avatar", "Updated avatar"),
                    ("create_article", "Created new article"),
                ],
                max_length=255,
            ),
        ),
    ]
