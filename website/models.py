from django.db import models

# Create your models here.

from django.db import models


class UserData(models.Model):
    username = models.CharField(max_length=16, primary_key=True)
    password = models.CharField(max_length=16)
    limits = models.IntegerField()
