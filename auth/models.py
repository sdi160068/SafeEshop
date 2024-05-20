import uuid
from django.conf import settings
from django.db import models

class User(models.Model):
    id = models.UUIDField(default = uuid.uuid4,primary_key=True)
    username = models.CharField(max_length=200,unique=True)
    password = models.CharField(max_length=200)
    REQUIRED_FIELDS = ["username", "password"]
    
    def __str__(self):
        return self.username
    
class Token(models.Model):
    id = models.UUIDField(default = uuid.uuid4,primary_key=True)
    token = models.CharField(max_length=200,unique=True)