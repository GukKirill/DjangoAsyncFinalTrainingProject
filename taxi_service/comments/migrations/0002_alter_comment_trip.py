# Generated by Django 4.1.7 on 2023-03-29 00:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0001_initial'),
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='trip',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='trips.trip'),
        ),
    ]
