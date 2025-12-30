from payments_app.models import Item


class ItemService:
    def get_item(self, id: int) -> Item:
        return Item.objects.get(id=id)
