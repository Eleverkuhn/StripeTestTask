from typing import override

from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from config import settings
from payments_app.services import ItemService, BuyService
from payments_app.models import Item


class ItemView(TemplateView):
    template_name = "item.xhtml"

    @override
    def get_context_data(self, id: int, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        item = ItemService().get_item(id)
        return self._generate_context(context, item)

    def _generate_context(self, context: dict, item: Item) -> dict:
        context["stripe_pk"] = settings.stripe_pk
        context["item_id"] = item.id
        context["title"] = item.name
        context["item"] = {field.verbose_name: getattr(item, field.name)
                           for field
                           in item._meta.fields}
        return context


class BuyView(View):
    def get(self, request, id: int, *args, **kwargs) -> JsonResponse:
        item = ItemService().get_item(id)
        session = BuyService(item).generate_stripe_session()
        return JsonResponse({"session_id": session.id})
