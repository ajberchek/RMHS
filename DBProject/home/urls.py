from django.conf.urls import include, url
from . import views
import os

urlpatterns = [
    url(r'^$', views.viewHome, name='vhome'),
    url(r'^ViewHouse',views.viewHouse),
    #url(os.path.join('SignIn'), include('SignIn.urls')),
    #url(os.path.join('SignUp'), include('SignUp.urls')),
]
