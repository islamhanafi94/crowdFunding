from django.db import models
from django.template.defaultfilters import slugify

from users.models import Users
# Create your models here.


class Categories(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Projects(models.Model):
    user = models.ForeignKey('users.Users', null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    details = models.CharField(max_length=100)
    category = models.ForeignKey('Categories', null=True, on_delete=models.CASCADE)
    total_target = models.IntegerField()
    start_date = models.DateField(auto_now=True)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    rating = models.FloatField()
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Tags(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Project_tags(models.Model):
    project = models.ForeignKey('Projects', null=True, on_delete=models.CASCADE)
    tag = models.ForeignKey('Tags', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.Tags.name


def get_image_name(instance, filename):
    title = instance.project.title
    slug = slugify(title)
    return "projects/images/%s-%s" % (slug, filename)


class Project_pics(models.Model):
    project = models.ForeignKey('Projects', null=True, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to=get_image_name, verbose_name='Project Image')

    def __str__(self):
        return str(self.project.title)


class Project_donations(models.Model):
    user = models.ForeignKey('users.Users', null=True, on_delete=models.CASCADE)
    project = models.ForeignKey('Projects', null=True, on_delete=models.CASCADE)
    donation = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.donation


class Project_comments(models.Model):
    user = models.ForeignKey('users.Users', null=True, on_delete=models.CASCADE)
    project = models.ForeignKey('Projects', null=True, on_delete=models.CASCADE)
    comment = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment


class Comment_replies(models.Model):
    user = models.ForeignKey('users.Users', null=True, on_delete=models.CASCADE)
    Comment = models.ForeignKey('Project_comments', null=True, on_delete=models.CASCADE)
    reply = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reply


class Project_rating(models.Model):
    user = models.ForeignKey('users.Users', null=True, on_delete=models.CASCADE)
    project = models.ForeignKey('Projects',null=True, on_delete=models.CASCADE)
    rating = models.FloatField()

    # def __str__(self):
    #     return self.rating


class Reports(models.Model):
    user = models.ForeignKey('users.Users', null=True, on_delete=models.CASCADE)
    project = models.ForeignKey('Projects', null=True, on_delete=models.CASCADE)
    Comment = models.ForeignKey('Project_comments', null=True, on_delete=models.CASCADE)
    report = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.report


