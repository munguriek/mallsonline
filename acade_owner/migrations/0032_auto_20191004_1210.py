# Generated by Django 2.2.3 on 2019-10-04 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acade_owner', '0031_auto_20190927_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='photo',
            field=models.ImageField(blank=True, default='owner_photos/default.png', null=True, upload_to='owner_photos'),
        ),
    ]
