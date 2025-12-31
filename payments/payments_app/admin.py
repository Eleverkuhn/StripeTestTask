from django.contrib import admin
from payments_app.models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fields = ["id", "name", "description", "price"]
    readonly_fields = ["id"]
