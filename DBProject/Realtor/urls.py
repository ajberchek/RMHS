from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^Houses/',views.housePage),
        url(r'^EditHouse',views.editHouse),
        url(r'^AddPic',views.addPicture),
        url(r'^CreateHouse',views.addHouse),
        url(r'^CreateRealtor',views.createRealtor),
        url(r'^ShowRealtor',views.showRealtor),
        url(r'^Review',views.review),
        url(r'^$',views.allRealtors),
]
