import uuid
from django.db import connection, models
from django.urls import reverse

from auth.models import User

class Product(models.Model):
    id = models.UUIDField(default = uuid.uuid4,primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    price = models.FloatField(default=0.0)
    REQUIRED_FIELDS = ["name", "price"]

    def __str__(self):
        return self.name
    
    def add_to_cart(self):
        return reverse("eshop:add_to_cart", kwargs={
            'id' : self.id
        })
    
class Cart(models.Model):
    id = models.UUIDField(default = uuid.uuid4,primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def getProducts(self):
        with connection.cursor() as cursor:
            # cursor.execute("SELECT name FROM eshop_orderedproduct")

            cursor.execute("""
                SELECT
                    eshop_product.name,
                    eshop_product.price,
                    eshop_orderedproduct.quantity,
                    eshop_orderedproduct.cart_id
                FROM
                    eshop_orderedproduct
                JOIN
                    eshop_product ON eshop_orderedproduct.product_id = eshop_product.id
                WHERE
                    eshop_orderedproduct.cart_id = %s;
                           """,[str(self.id.hex)])

            data = cursor.fetchall()

        return data
    
class OrderedProduct(models.Model):
    product_id = models.UUIDField(default = uuid.uuid4)
    cart_id = models.UUIDField(default = uuid.uuid4)
    quantity = models.PositiveIntegerField(default=0)
    REQUIRED_FIELDS = ["cart_id", "product_id"]
