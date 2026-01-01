from django.contrib import admin
from payments_app.models import Item, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fields = ["id", "name", "description", "price"]
    readonly_fields = ["id"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ["id", "items"]
    readonly_fields = ["id"]
