# Generated by Django 4.1.7 on 2023-04-10 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_alter_comment_trip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='about_car',
            field=models.TextField(default=None, max_length=250),
        ),
        migrations.AlterField(
            model_name='comment',
            name='about_driver',
            field=models.TextField(default=None, max_length=250),
        ),
    ]
