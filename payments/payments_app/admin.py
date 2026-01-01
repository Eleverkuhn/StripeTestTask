from django.contrib import admin
from payments_app.models import Item, Discount, Tax, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fields = ["id", "name", "description", "price"]
    readonly_fields = ["id"]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    fields = ["id", "value"]
    readonly_fields = ["id"]


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    fields = ["id", "value"]
    readonly_fields = ["id"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ["id", "items", "tax", "discount"]
    readonly_fields = ["id"]
