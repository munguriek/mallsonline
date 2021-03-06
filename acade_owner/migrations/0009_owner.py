# Generated by Django 2.2.3 on 2019-09-18 07:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('acade_owner', '0008_auto_20190917_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_rooms', models.IntegerField()),
                ('name', models.CharField(max_length=200, verbose_name='Owner Name')),
                ('address', models.CharField(max_length=200, verbose_name='Owner Address')),
                ('email', models.CharField(max_length=200, verbose_name='Owner Email Address')),
                ('phone', models.CharField(max_length=200, verbose_name='Owner Phone Number')),
                ('photo', models.ImageField(blank=True, default='Owner_photos/default.png', null=True, upload_to='owner_photos')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('acade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acade_owner.Acade', verbose_name='Building')),
                ('floor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acade_owner.Floor', verbose_name='Floor Owned')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
