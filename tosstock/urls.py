from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework.permissions import AllowAny

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('dj_rest_auth.urls')),
    path('api/v1/accounts/signup/', include('dj_rest_auth.registration.urls')),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/boards/', include('boards.urls')),
    path('api/v1/news/', include('news.urls')),
]