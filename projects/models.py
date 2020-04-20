from django.db import models

# Create your models here.

class Categories(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Projects(models.Model):
    title = models.CharField(max_length=50)
    details = models.CharField(max_length=100)
    category = models.ForeignKey('Categories',null=True ,on_delete=models.CASCADE)
    total_target = models.IntegerField(min_value=0)
    start_date = models.DateField(auto_now=True)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    rating = models.FloatField(max_value=5, min_value=0)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Tags(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Project_tags(models.Model):
    project = models.ForeignKey('Projects', null=True, on_delete=models.CASCADE)
    tag = models.ForeignKey('Tags', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Project_pics(models.Model):
    project = models.ForeignKey('Projects', null=True, on_delete=models.CASCADE)
    pic = models.CharField(max_length=50)

    def __str__(self):
            return self.name

class Project_donations(models.Model):
    project = models.ForeignKey('Projects', null=True, on_delete=models.CASCADE)
    donation = models.IntegerField(min_value=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return self.name

class Project_comments(models.Model):
    project = models.ForeignKey('Projects', null=True, on_delete=models.CASCADE)
    comment = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return self.name

class Comment_replies(models.Model):
    Comment = models.ForeignKey('Comments', null=True, on_delete=models.CASCADE)
    reply = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return self.name


class Rating(models.Model):
    project = models.ForeignKey('Projects', null=True, on_delete=models.CASCADE)
    rating = models.FloatField(max_value=5, min_value=0)

    def __str__(self):
            return self.name

class Reports(models.Model):
    project = models.ForeignKey('Projects', null=True, on_delete=models.CASCADE)
    Comment = models.ForeignKey('Comments', null=True, on_delete=models.CASCADE)
    report = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return self.name


