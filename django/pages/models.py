from django.db import models

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=100)

class UserProfile(models.Model):
    user = models.CharField(max_length=100)
    pontuation = models.IntegerField(default=0)
