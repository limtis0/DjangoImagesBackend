from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=22)
    title = models.CharField(max_length=128)
    width = models.IntegerField()
    height = models.IntegerField()
