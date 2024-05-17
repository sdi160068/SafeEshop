from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    price = models.FloatField(default=0.0)
    REQUIRED_FIELDS = ["name", "price"]

    def __str__(self):
        return self.name