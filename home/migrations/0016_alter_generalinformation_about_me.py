# Generated by Django 4.2.7 on 2023-12-30 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_generalinformation_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalinformation',
            name='about_me',
            field=models.TextField(verbose_name='Introduction about the user'),
        ),
    ]