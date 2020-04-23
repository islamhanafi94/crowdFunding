from django.urls import path
from .views import home 

urlpatterns = [
    path('home', home, name='all_projects'),
    # path('showCategory/<int:id>',list_categories ,name="show_cate"),
    ]
