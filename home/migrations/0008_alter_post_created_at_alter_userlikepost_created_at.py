# Generated by Django 4.2.7 on 2023-12-27 14:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_remove_post_total_likes_alter_post_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 27, 14, 47, 5, 492349, tzinfo=datetime.timezone.utc), editable=False),
        ),
        migrations.AlterField(
            model_name='userlikepost',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 27, 14, 47, 5, 493276, tzinfo=datetime.timezone.utc)),
        ),
    ]
