import stripe
from stripe import Price
from stripe.checkout import Session

from config import settings
from payments_app.models import Item


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


class ItemService:
    def get_item(self, id: int) -> Item:
        return Item.objects.get(id=id)
