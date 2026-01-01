from typing import override

from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.db.models import Model

from config import settings
from payments_app.services import (CheckoutItemService,
                                   CheckoutOrderService,
                                   BaseCheckoutService)
from payments_app.models import Item, Order


class BaseBuyView(View):
    model: type[Model]
    service: type[BaseCheckoutService]

    def get(self, request, id: int, *args, **kwargs) -> JsonResponse:
        order = get_object_or_404(self.model, id=id)
        session = self.service(order).generate_stripe_session()
        return JsonResponse({"id": session.id})


class ItemView(TemplateView):
    template_name = "item.xhtml"

    @override
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = get_object_or_404(Item, id=self.kwargs["id"])
        return self._generate_context(context, item)

    def _generate_context(self, context: dict, item: Item) -> dict:
        context["stripe_pk"] = settings.stripe_pk
        context["item_id"] = item.id
        context["title"] = item.name
        context["item"] = {field.verbose_name: getattr(item, field.name)
                           for field
                           in item._meta.fields}
        return context


class OrderView(TemplateView):
    template_name = "order.xhtml"

    @override
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = get_object_or_404(Order, id=self.kwargs["id"])
        return self._generate_context(context, order)

    def _generate_context(self, context: dict, order: Order) -> dict:
        context["stripe_pk"] = settings.stripe_pk
        context["order_id"] = order.id
        context["total_price"] = order.total_price
        context["order"] = {item.name: item.price
                            for item
                            in order.items.all()}
        return context


class BuyOrderView(BaseBuyView):
    model = Order
    service = CheckoutOrderService


class BuyItemView(BaseBuyView):
    model = Item
    service = CheckoutItemService
