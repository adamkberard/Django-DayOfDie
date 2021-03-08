from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('game/', include('apps.games.urls')),
    path('auth/', include('apps.my_auth.urls')),
]
