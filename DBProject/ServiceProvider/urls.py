from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^CreateServiceProvider', views.CreateServiceProvder),
    url(r'^ViewServices',views.ViewServices),
    url(r'^ViewService',views.ViewService),
]
