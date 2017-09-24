from django.conf.urls import url
from board.views import boardLV, BoardCreate

urlpatterns = [
     url(r'^seeboard/$', boardLV.as_view(), name='seeboard'),
     url(r'^writeboard/$', BoardCreate, name='writeboard'),
]