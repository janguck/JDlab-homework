from django.conf.urls import url
from account.views import SignUpview



urlpatterns = [
    url(r'^signup/$', SignUpview.as_view(), name='signup'),
    url(r'^login/$', SignUpview.as_view(), name='login'),

    #url(r'^account/', include('account.urls')),

]
