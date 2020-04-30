from django.urls import path
from . import views 

app_name = 'projects'

urlpatterns = [
    # path('home', home, name='all_projects'),
    path('new', views.create_project, name='new_project'),
    path('<int:id>', views.project_page, name='project_page'),
    path('<int:id>/cancel', views.cancel_project, name='cancel_project'),
    path('<int:id>/rating/<int:rate>', views.project_rating, name='project_rating'),
    path('comment/<project_id>', views.comment, name='comment'),
    # path('<int:id>/pics', views.Project_pics, name='project_pics')
    ]
