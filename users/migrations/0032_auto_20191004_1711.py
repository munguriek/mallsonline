# Generated by Django 2.2.3 on 2019-10-04 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0031_auto_20191004_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='actual_price',
            field=models.IntegerField(default=1, verbose_name='Sold at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='users.ProductStatus'),
        ),
    ]
