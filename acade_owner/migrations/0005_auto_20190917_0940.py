# Generated by Django 2.2.3 on 2019-09-17 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acade_owner', '0004_auto_20190913_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='acade',
            name='no_of_floors',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='acade',
            name='no_of_rooms',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
