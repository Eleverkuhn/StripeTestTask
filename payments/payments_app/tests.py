from django.urls import reverse
from django.test import TestCase

from logger.setup import LoggingConfig
from payments_app.models import Item


class TestItemView(TestCase):
    fixtures = ["items"]
    url = reverse("item", kwargs={"id": 1})

    def test_exists(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_is_used(self) -> None:
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "item.xhtml")

    def test_contains_item_info(self) -> None:
        response = self.client.get(self.url)
        item = Item.objects.get(id=1)
        for field in item._meta.get_fields():
            if field.concrete:
                field_value = getattr(item, field.name)
                self.assertIn(str(field_value), response.content.decode())


class TestBuyView(TestCase):
    fixtures = ["items"]
    url = reverse("buy", kwargs={"id": 1})

    def test_output(self) -> None:  # INFO: for debug
        response = self.client.get(self.url)
        LoggingConfig().logger.debug(response.content.decode())
