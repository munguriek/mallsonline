# Generated by Django 2.2.6 on 2020-05-11 07:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('acade_owner', '0032_auto_20191004_1210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rent',
            name='month',
        ),
        migrations.RemoveField(
            model_name='rent',
            name='year',
        ),
        migrations.AddField(
            model_name='rent',
            name='rent_from',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='rent',
            name='rent_to',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
