from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Photo(models.Model):
    photo_username = models.IntegerField(primary_key=True)
    count = models.IntegerField()
    image = models.CharField(max_length=200)
    price = models.IntegerField()
    photo_description = models.CharField(max_length=200)

class Action(models.Model):
    action_user_username = models.ForeignKey(settings.AUTH_USER_MODEL,to_field='username')
    action_photo_username = models.ForeignKey(Photo)
    action_type = models.CharField(max_length=200)

class Favorite_Photo(models.Model):
    favorite_user_username = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='username')
    favorite_photo_username = models.ForeignKey(Photo)
    boolean = models.CharField(max_length=200)

