# Generated by Django 2.2.3 on 2019-09-24 12:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('acade_owner', '0015_auto_20190924_1548'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='employee',
            unique_together={('user', 'acade', 'nin')},
        ),
    ]
