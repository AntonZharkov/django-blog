# Generated by Django 4.2.2 on 2023-06-28 08:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0003_article_tags"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="blog.comment",
            ),
        ),
    ]
