from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$',views.accountPage,name = 'index'),
        url(r'^EditAccount/',views.editAccount),
]
