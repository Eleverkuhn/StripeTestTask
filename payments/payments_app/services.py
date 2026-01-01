from typing import override

import stripe
from stripe import Price, Coupon, TaxRate
from stripe.checkout import Session

from config import settings
from payments_app.models import Item, Order


class BaseCheckoutService:
    domain = f"http://{settings.django_host}:{settings.django_port}"

    def __init__(self) -> None:
        stripe.api_key = settings.stripe_sk
        stripe.api_version = "2025-12-15.clover"
        self.session_data = {"ui_mode": "custom",
                             "mode": "payment",
                             "return_url": self.domain}

    def construct_stripe_session(self,
                                 line_items: list[dict],
                                 coupon: Coupon | None = None) -> Session:
        self.session_data["line_items"] = line_items
        if coupon:
            self.session_data["discounts"] = [{"coupon": coupon.id}]
        return stripe.checkout.Session.create(**self.session_data)


class CheckoutOrderService(BaseCheckoutService):
    @override
    def __init__(self, order: Order) -> None:
        super().__init__()
        self.order = order

    def generate_stripe_session(self) -> Session:
        line_items = self.generate_line_items()
        coupon = self.generate_coupon()
        session = self.construct_stripe_session(line_items, coupon)
        return session

    def generate_line_items(self) -> list[dict]:
        line_items = []
        tax = self.generate_tax()

        for item in self.order.items.all():
            self.populate_line_items(line_items, item, tax)

        return line_items

    def populate_line_items(self,
                            line_items: list,
                            item: Item,
                            tax: TaxRate | None) -> None:
        line_item = CheckoutItemService(item).construct_line_item()
        self.add_tax(line_item, tax)
        line_items.append(line_item)

    def add_tax(self, line_item: dict, tax: TaxRate | None) -> None:
        if tax:
            line_item["tax_rates"] = [tax.id]

    def generate_coupon(self) -> Coupon | None:
        if self.order.discount:
            coupon = stripe.Coupon.create(percent_off=self.order.discount.value,
                                          duration="once")
            return coupon

    def generate_tax(self) -> TaxRate | None:
        if self.order.tax:
            tax = stripe.TaxRate.create(display_name="НДС",
                                        description="Налог на добавочную стоимость",
                                        jurisdiction="RU",
                                        percentage=self.order.tax.value,
                                        inclusive=False)
            return tax


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
