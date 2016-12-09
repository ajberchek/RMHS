from django.conf.urls import include, url
from . import views
import os

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
