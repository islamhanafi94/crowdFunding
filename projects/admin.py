from django.contrib import admin
from .models import Categories , Projects
from django.contrib.auth.models import Group


# Register your models here.

admin.site.site_header = "Crowd Fund Admin Panel"

class New_Project(admin.ModelAdmin):
    exclude = ('rating','user','title','details','category','total_target','end_date')
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Categories)
admin.site.register(Projects,New_Project)
admin.site.unregister(Group)