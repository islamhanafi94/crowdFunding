# Generated by Django 3.0.5 on 2020-04-20 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='mobile_phone',
            new_name='phone',
        ),
    ]