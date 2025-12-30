from django.db import models
from django.core.validators import MinLengthValidator


class Item(models.Model):
    name = models.CharField(max_length=80, validators=[MinLengthValidator(1)])
    description = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = "items"

    def __repr__(self) -> str:
        return f"{self.name}"
