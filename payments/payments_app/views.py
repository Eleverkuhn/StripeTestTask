from typing import override

from django.http.response import HttpResponse
from django.views import View
from django.views.generic import TemplateView

from payments_app.services import ItemService, BuyService


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


class BuyView(View):
    def get(self, request, id: int, *args, **kwargs):
        item = ItemService().get_item(id)
        session = BuyService(item).generate_stripe_session()
        return HttpResponse(session.id)
