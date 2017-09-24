from django.conf.urls import url, include
from django.contrib import admin

from blissray.views import Home

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home', Home.as_view(), name='home'),
    url(r'^$', Home.as_view(), name='home'),

    url(r'^account/', include('account.urls')),
    url(r'^board/', include('board.urls')),
    url(r'^shopping/', include('shopping.urls')),

]
