from django.urls import path
from users.views import test, register_view, activate, login_view, logout_view
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url


app_name = 'users'

urlpatterns = [
    path('', test, name='users'),
    path('register', register_view, name='register'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/$',
        activate, name='activate'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
