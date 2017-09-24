from django.conf.urls import url
from shopping.views import PhotoLV,buyphoto, BuyLV, refundphoto, favorite_photo, see_favorite_photo, cancel_photo

urlpatterns = [
     url(r'^seephoto/$', PhotoLV.as_view(), name='seephoto'),
     url(r'^buyphoto/$', buyphoto, name='buyphoto'),
     url(r'^buy_receipt/$', BuyLV, name='buy_receipt'),
     url(r'^refundphoto/$', refundphoto, name='refundphoto'),
     url(r'^favorite_photo/$', favorite_photo, name='favorite_photo'),
     url(r'^see_favorite_photo/$', see_favorite_photo, name='see_favorite_photo'),
     url(r'^cancelfavorite/$', cancel_photo, name='cancelfavorite'),

]