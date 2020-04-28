from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator

class MyUserManger(BaseUserManager):
    def create_user(self, email, first_name,last_name,phone,photo, password=None):
        if not email:
            raise ValueError("users must have an email...")
        if not first_name:
            raise ValueError('user must have a first name...')
        if not last_name:
            raise ValueError('user must have a last name...')
        if not phone:
            raise ValueError('user must have a phone...')
        if not photo:
            raise ValueError('user must have a photo...')

        user = self.model(email=self.normalize_email(email),first_name = first_name,last_name=last_name,phone=phone,photo=photo)

        user.set_password(password)


        user.save(using=self._db)
        return user

    def create_superuser(self, email,first_name,last_name,phone,photo,password):
        user = self.create_user(email=self.normalize_email(email),
                          password=password,
                          first_name=first_name,
                          last_name=last_name,
                          phone=phone,photo=photo)

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user





# Create your models here.
class Users(AbstractBaseUser):
    phone_regex = RegexValidator(regex=r'^01[1|0|2|5][0-9]{8}$',message='phone must be an egyptian phone number...')
    first_name = models.CharField(verbose_name="first_name" ,null=False, max_length=50)
    last_name = models.CharField(verbose_name= "last_name" ,null=False, max_length=50)
    email = models.EmailField(verbose_name='email', null=False, max_length=254,unique=True)
    phone = models.CharField(verbose_name="phone",null=True,validators=[phone_regex],max_length=14)
    photo = models.ImageField(verbose_name="photo",upload_to='users/images')
    date_birth = models.DateField(null=True)
    facebook_link = models.URLField(null=True)
    country = models.CharField(max_length=50, null=True)
    date_joined = models.DateTimeField(verbose_name="date_joined",
                                       auto_now=True)
    last_login = models.DateTimeField(verbose_name="last_login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name','last_name','phone','photo']

    objects = MyUserManger()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

