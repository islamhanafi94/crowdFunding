from django.urls import path
from  users.views import test,register_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', test, name='users'),
    path('register',register_view,name='register')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)