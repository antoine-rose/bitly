from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

from .views import urlList, Home, redirect

urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('admin/', admin.site.urls),
    url('API/', urlList.as_view()),
    url(r'', redirect, name='redirect'),

]