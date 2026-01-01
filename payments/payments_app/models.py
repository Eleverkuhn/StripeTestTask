from decimal import Decimal

from django.db import models
from django.core.validators import (MinLengthValidator,
                                    MinValueValidator,
                                    MaxLengthValidator)


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


class Discount(models.Model):
    value = models.IntegerField(validators=[MaxLengthValidator(100)],
                                default=0)

    class Meta:
        db_table = "discounts"

    def __str__(self) -> str:
        return f"{self.value} %"


class Tax(models.Model):
    value = models.IntegerField(validators=[MaxLengthValidator(100)],
                                default=0)

    class Meta:
        db_table = "taxes"

    def __str__(self) -> str:
        return f"{self.value} %"


class Order(models.Model):
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(Discount,
                                 on_delete=models.SET_NULL,
                                 null=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "orders"

    def __str__(self) -> str:
        return f"Order {self.id}: {', '.join(item.name for item in self.items.all())}, {self.total_price}"

    @property
    def total_price(self) -> Decimal:
        total_price = sum(item.price for item in self.items.all())
        if self.discount:
            total_price = total_price * self.discount.value / 100
        if self.tax:
            total_price = total_price * self.tax.value / 100
        return total_price
