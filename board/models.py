from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class board(models.Model):
    board_user_username = models.ForeignKey(settings.AUTH_USER_MODEL,to_field='username')
    board_description = models.CharField(max_length=200)