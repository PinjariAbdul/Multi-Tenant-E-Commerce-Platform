from django.db import models
from tenants.models import Tenant
from accounts.models import User


class Product(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.name)


class Order(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def total_price(self):
        # Access the actual price value from the related product
        if self.product and self.product.price:
            return int(self.quantity) * float(str(self.product.price))
        return 0.0
        
    def __str__(self):
        return f"Order {self.pk} - {self.product.name}"