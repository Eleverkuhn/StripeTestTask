from typing import override

import stripe
from stripe import Price
from stripe.checkout import Session

from config import settings
from payments_app.models import Item, Order


class BaseCheckoutService:
    domain = f"http://{settings.django_host}:{settings.django_port}"

    def __init__(self) -> None:
        stripe.api_key = settings.stripe_sk
        stripe.api_version = "2025-12-15.clover"

    def construct_stripe_session(self, line_items: list[dict]) -> Session:
        return stripe.checkout.Session.create(ui_mode="custom",
                                              line_items=line_items,
                                              mode="payment",
                                              return_url=self.domain)


class CheckoutOrderService(BaseCheckoutService):
    @override
    def __init__(self, order: Order) -> None:
        super().__init__()
        self.order = order

    def generate_stripe_session(self) -> Session:
        line_items = self.generate_line_items()
        session = self.construct_stripe_session(line_items)
        return session

    def generate_line_items(self) -> list[dict]:
        return [CheckoutItemService(item).construct_line_item()
                for item
                in self.order.items.all()]


class CheckoutItemService(BaseCheckoutService):
    @override
    def __init__(self, item: Item) -> None:
        super().__init__()
        self.item = item

    @property
    def converted_price(self) -> int:
        return int(self.item.price * 100)

    def generate_stripe_session(self) -> Session:
        line_items = [self.construct_line_item()]
        session = self.construct_stripe_session(line_items)
        return session

    def construct_line_item(self) -> dict[str, str | int]:
        return {"price": self.generate_price().id, "quantity": 1}

    def generate_price(self) -> Price:
        product = stripe.Product.create(name=self.item.name)
        price = stripe.Price.create(product=product.id,
                                    unit_amount=self.converted_price,
                                    currency="rub")
        return price
