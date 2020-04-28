from django.urls import path
from .views import home, project , donate , comment

urlpatterns = [
    path('home', home, name='all_projects'),
    # path('showCategory/<int:id>',list_categories ,name="show_cate"),
    path('<int:project_id>', project, name='project'),
    path('<int:project_id>/donate/', donate, name='donate'),
    path('<int:project_id>/comment/', comment, name='comment'),
    ]
