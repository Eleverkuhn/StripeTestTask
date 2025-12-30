from typing import override

from django.views.generic import TemplateView

from payments_app.services import ItemService


class ItemView(TemplateView):
    template_name = "item.xhtml"

    @override
    def get_context_data(self, id: int, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        item = ItemService().get_item(id)
        context["item"] = [{"name": field.verbose_name,
                            "value": getattr(item, field.name)}
                           for field
                           in item._meta.fields]
        return context
