# Generated by Django 3.0.5 on 2020-04-20 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('first_name', models.CharField(max_length=50, verbose_name='first_name')),
                ('last_name', models.CharField(max_length=50, verbose_name='last_name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('mobile_phone', models.IntegerField(null=True, verbose_name='phone')),
                ('profile_pic', models.ImageField(blank=True, upload_to='static/', verbose_name='photo')),
                ('date_birth', models.DateField(null=True)),
                ('facebook_link', models.URLField(null=True)),
                ('country', models.CharField(default='', max_length=50)),
                ('date_joined', models.DateTimeField(auto_now=True, verbose_name='date_joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last_login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]