from decimal import Decimal
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


class CheckoutOrderService(BaseCheckoutService):
    @override
    def __init__(self, order: Order) -> None:
        super().__init__()
        self.order = order

    def generate_stripe_session(self) -> Session:
        session = stripe.checkout.Session.create(
            ui_mode="custom",
            line_items=self.generate_line_items(),
            mode="payment",
            return_url=self.domain
        )
        return session

    def generate_line_items(self) -> list[dict]:
        return [
            {"price": BuyService(item).generate_price().id, "quantity": 1}
            for item
            in self.order.items.all()
        ]


class BuyService:
    domain = f"http://{settings.django_host}:{settings.django_port}"

    def __init__(self, item: Item) -> None:
        self.item = item
        stripe.api_key = settings.stripe_sk
        stripe.api_version = "2025-12-15.clover"

    @property
    def converted_price(self) -> int:
        return int(self.item.price * 100)

    def generate_stripe_session(self) -> Session:
        price = self.generate_price()

        session = stripe.checkout.Session.create(
            ui_mode="custom",
            line_items=[{"price": price.id, "quantity": 1}],
            mode="payment",
            return_url=self.domain
        )

        return session

    def generate_price(self) -> Price:
        product = stripe.Product.create(name=self.item.name)
        price = stripe.Price.create(product=product.id,
                                    unit_amount=self.converted_price,
                                    currency="rub")
        return price
