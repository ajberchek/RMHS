from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^Houses/',views.housePage),
        url(r'^EditHouse',views.editHouse),
        url(r'^AddPic',views.addPicture),
        url(r'^CreateHouse',views.addHouse),
]
