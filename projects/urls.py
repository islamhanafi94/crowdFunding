from django.urls import path
<<<<<<< HEAD
from .views import home, project , donate , comment

urlpatterns = [
    path('home', home, name='all_projects'),
    # path('showCategory/<int:id>',list_categories ,name="show_cate"),
    path('<int:project_id>', project, name='project'),
    path('<int:project_id>/donate/', donate, name='donate'),
    path('<int:project_id>/comment/', comment, name='comment'),
=======
from . import views 

urlpatterns = [
    # path('home', home, name='all_projects'),
    path('<int:id>', views.project_page, name='project_page'),
    path('<int:id>/cancel', views.cancel_project, name='cancel_project'),
    path('<int:id>/rating/<int:rate>', views.project_rating, name='project_rating') 
>>>>>>> 6737ed8dfda2e7c73d0e35a3efb52348052a8392
    ]
