# Generated by Django 4.2.7 on 2023-12-30 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_alter_generalinformation_gender_alter_post_caption_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalinformation',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, verbose_name='Phone number of user'),
        ),
    ]
