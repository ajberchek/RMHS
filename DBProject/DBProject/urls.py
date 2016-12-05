from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', admin.site.urls),
    url(r'^SignIn/', include('SignIn.urls')),
    url(r'^SignUp/', include('SignUp.urls')),
    url(r'^Account/', include('AccountPage.urls')),
    url(r'^Logout/',include('Logout.urls')),

]
