# Generated by Django 4.1.7 on 2023-04-11 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxi_depot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='free',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='driver',
            name='free',
            field=models.BooleanField(default=True),
        ),
    ]