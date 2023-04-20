# Generated by Django 4.1.7 on 2023-03-28 22:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taxi_depot', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('end', models.DateTimeField()),
                ('start_point', models.CharField(max_length=20)),
                ('end_point', models.CharField(max_length=20)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxi_depot.car')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxi_depot.driver')),
            ],
        ),
    ]