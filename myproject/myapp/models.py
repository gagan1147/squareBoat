from random import random
from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE


from django.contrib.auth.models import User

# Create your models here.

# User = settings.AUTH_USER_MODEL

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE)
    follower = models.ManyToManyField(User,related_name="follower")

class Tweets(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=CASCADE)
    content = models.TextField(blank=True,null=True)
    

    class Meta:
        ordering = ['-id']
    