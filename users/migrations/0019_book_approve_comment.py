# Generated by Django 2.2.3 on 2019-09-23 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_book_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='approve_comment',
            field=models.TextField(default=1, verbose_name='Add a comment'),
            preserve_default=False,
        ),
    ]