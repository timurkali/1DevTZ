from django.db import models
from django.contrib.auth import get_user_model

from basic import constants as const

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.pk} | {self.name}'


class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.IntegerField()
    amount = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f'{self.pk} | {self.name}'


class Order(models.Model):
    total = models.PositiveIntegerField(default=0)
    currency = models.CharField(
        max_length=64,
        choices=const.CURRENCIES.choices,
        default=const.CURRENCIES.TIYN
    )
    status = models.CharField(
        max_length=32,
        choices=const.ORDER_STATUSES.choices,
        default=const.ORDER_STATUSES.NEW
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')

    def get_exist_products(self):
        return [order_line.product_id for order_line in self.order_lines.all()]

    def get_total_in_kzt(self):
        return (self.total / 100)


class OrderLine(models.Model):
    count = models.PositiveIntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_lines')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_lines')

    class Meta:
        unique_together = ('product', 'order')
