from django.conf.urls import url
from account.views import SignUpView, LogOutView, LoginView, UserListView

urlpatterns = [
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogOutView.as_view(), name='logout'),
    url(r'^profile/$', UserListView.as_view(), name='profile'),

]
