# Generated by Django 3.0.5 on 2020-04-21 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200420_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='photo',
            field=models.ImageField(upload_to='users/images', verbose_name='photo'),
        ),
    ]
