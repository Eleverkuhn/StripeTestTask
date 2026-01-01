from decimal import Decimal

from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator


class Item(models.Model):
    name = models.CharField(max_length=80, validators=[MinLengthValidator(1)])
    description = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                validators=[MinValueValidator(Decimal("1.00"))])

    class Meta:
        db_table = "items"

    def __repr__(self) -> str:
        return f"{self.name}"

    def __str__(self) -> str:
        return f"{self.name}"


class Order(models.Model):
    items = models.ManyToManyField(Item)

    class Meta:
        db_table = "orders"

    def __str__(self) -> str:
        return f"Order {self.id}: {', '.join(item.name for item in self.items.all())}, {self.total_price}"

    @property
    def total_price(self) -> Decimal:
        return sum(item.price for item in self.items.all())
