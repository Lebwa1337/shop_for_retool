import os
import uuid

from django.db import models
from django.utils.text import slugify

from users.models import User


class Brand(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


def create_custom_path(instance, filename):
    _, extension = os.path.splitext(filename)
    return os.path.join(
        "uploads", "img",
        f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"
    )


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(
        upload_to=create_custom_path,
        blank=True,
        null=True
    )

    @property
    def characteristics(self):
        return {pc.characteristic.name: pc.value for pc in self.product_characteristics.all()}

    def __str__(self):
        return self.name


class Characteristic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProductCharacteristic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_characteristics')
    characteristic = models.ForeignKey(Characteristic, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product.name} - {self.characteristic.name}: {self.value}"


class Order(models.Model):
    class StatusChoices(models.Choices):
        PENDING = 'PENDING'
        COMPLETED = 'COMPLETED'
        CANCELLED = 'CANCELLED'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product)
    status = models.CharField(choices=StatusChoices.choices, default=StatusChoices.PENDING, max_length=50)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)




