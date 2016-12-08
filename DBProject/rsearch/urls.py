from django.conf.urls import include, url
from . import views
import os

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^ViewHouse',views.viewHouse),
    #url(os.path.join('SignIn'), include('SignIn.urls')),
    #url(os.path.join('SignUp'), include('SignUp.urls')),
]
