# Generated by Django 4.2.7 on 2023-12-25 13:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_post_created_at_userlikepost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 25, 13, 35, 33, 444484, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='userlikepost',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 25, 13, 35, 33, 445546, tzinfo=datetime.timezone.utc)),
        ),
    ]
