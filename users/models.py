from django.db import models


# Create your models here.
class Users(models.Model):
    first_name = models.CharField(null=False, max_length=50)
    last_name = models.CharField(null=False, max_length=50)
    email = models.EmailField(null=False, max_length=254)
    password = models.CharField(null=False, max_length=50)
    active = models.BooleanField(default=False)
    mobile_phone = models.IntegerField(null=True, max_length=12)
    profile_pic = models.CharField(blank=True)
    date_birth = models.DateField(null=True)
    facebook_link = models.URLField(null=True)
    country = models.CharField(max_length=50, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.name

