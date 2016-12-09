from django.conf.urls import include, url
from django.contrib import admin
from home import views

urlpatterns = [
    url(r'^$',views.viewHome),
    url(r'^admin/', admin.site.urls),
    url(r'^home/', include('home.urls')),
    url(r'^rsearch/',include('rsearch.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^rsearch/', include('rsearch.urls')),
    url(r'^SignIn/', include('SignIn.urls')),
    url(r'^SignUp/', include('SignUp.urls')),
    url(r'^Account/', include('AccountPage.urls')),
    url(r'^Logout/',include('Logout.urls')),
    url(r'^Realtor/',include('Realtor.urls')),
    url(r'^ServiceProvider/',include('ServiceProvider.urls')),
]
