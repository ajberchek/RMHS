from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', admin.site.urls),
    url(r'^SignIn/', include('SignIn.urls')),
    url(r'^SignUp/', inWclude('SignUp.urls')),

]
