# Generated by Django 2.2.3 on 2019-09-23 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_auto_20190923_1529'),
    ]

    operations = [
        migrations.CreateModel(
            name='TenantStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]
