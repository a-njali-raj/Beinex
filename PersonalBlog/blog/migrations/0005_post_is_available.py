# Generated by Django 5.1 on 2024-08-23 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_remove_post_tags_post_tag_delete_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
