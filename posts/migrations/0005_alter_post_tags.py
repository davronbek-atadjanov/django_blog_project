# Generated by Django 5.0.7 on 2024-07-21 13:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0004_remove_hitcount_ip_address_hitcount_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(related_name="tags", to="posts.tags"),
        ),
    ]
