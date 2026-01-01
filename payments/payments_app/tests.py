from django.urls import reverse
from django.test import TestCase

from logger.setup import LoggingConfig
from payments_app.views import ItemView, OrderView
from payments_app.models import Item, Order


class BaseTestView:
    url: str
    template: str

    def test_exists(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_is_used(self) -> None:
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, self.template)


class TestItemView(TestCase, BaseTestView):
    fixtures = ["items"]
    url = reverse("item", kwargs={"id": 1})
    template = ItemView.template_name

    def test_contains_item_info(self) -> None:
        response = self.client.get(self.url)
        item = Item.objects.get(id=1)
        for field in item._meta.get_fields():
            if field.concrete:
                field_value = getattr(item, field.name)
                self.assertIn(str(field_value), response.content.decode())


class TestOrderView(TestCase, BaseTestView):
    fixtures = ["items", "orders"]
    url = reverse("order", kwargs={"id": 1})
    template = OrderView.template_name

    def test_contains_order_info(self) -> None:
        response = self.client.get(self.url)
        order = Order.objects.get(id=1)
        content = response.content.decode()

        self.assertIn(str(order.total_price), content)
        for item in order.items.all():
            self.assertIn(item.name, content)
            self.assertIn(str(item.price), content)


class TestBuyView(TestCase):
    fixtures = ["items"]
    url = reverse("buy", kwargs={"id": 1})

    def test_output(self) -> None:  # INFO: for debug
        response = self.client.get(self.url)
        LoggingConfig().logger.debug(response.content.decode())
