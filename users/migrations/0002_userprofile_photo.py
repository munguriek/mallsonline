# Generated by Django 2.2.3 on 2019-08-30 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to='user_photos'),
        ),
    ]
