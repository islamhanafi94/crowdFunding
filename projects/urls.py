from django.urls import path
from . import views 

urlpatterns = [
    # path('home', home, name='all_projects'),
    path('<int:id>', views.project_page, name='project_page'),
    path('<int:id>/cancel', views.cancel_project, name='cancel_project'),
    path('<int:id>/rating/<int:rate>', views.project_rating, name='project_rating') 
    ]
