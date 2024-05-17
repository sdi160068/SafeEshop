from django.conf import settings
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=200,unique=True)
    password = models.CharField(max_length=200)
    REQUIRED_FIELDS = ["username", "password"]
    

    def __str__(self):
        return self.username
