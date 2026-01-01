import json

from django.urls import reverse
from django.test import TestCase

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


class BaseTestBuyView:
    url: str

    def test_returns_session_id(self) -> None:
        response = self.client.get(self.url)
        content = json.loads(response.content.decode("utf-8"))
        self.assertTrue(content.get("id"))


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
    fixtures = ["items", "discounts", "taxes", "orders"]
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


class TestBuyItemView(TestCase, BaseTestBuyView):
    fixtures = ["items"]
    url = reverse("buy_item", kwargs={"id": 1})


class TestBuyOrderView(TestCase, BaseTestBuyView):
    fixtures = ["items", "discounts", "taxes", "orders"]
    url = reverse("buy_order", kwargs={"id": 1})
