# Django modules
from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    DecimalField,
    PositiveIntegerField,
    BooleanField,
    DateTimeField,
    UniqueConstraint,
    CASCADE,
    SET_NULL,
)
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

# Project modules
from apps.catalogs.models import Restaurant, MenuItem

User = get_user_model()


class Address(Model):
    """
    Address database (table) model.
    """

    user = ForeignKey(
        to=User,
        on_delete=CASCADE,
        related_name="addresses",
    )
    street = CharField(max_length=255)
    city = CharField(max_length=100)
    postal_code = CharField(max_length=20)
    country = CharField(max_length=100)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    deleted_at = DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.street}, {self.city}"


class PromoCode(Model):
    """
    PromoCode database (table) model.
    """

    CODE_MAX_LEN = 50

    code = CharField(max_length=CODE_MAX_LEN, unique=True)
    discount_percent = DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    is_active = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.code


class Order(Model):
    """
    Order database (table) model.
    """

    STATUS_NEW = 1
    STATUS_CONFIRMED = 2
    STATUS_DELIVERING = 3
    STATUS_DONE = 4

    STATUS_CHOICES = {
        STATUS_NEW: "New",
        STATUS_CONFIRMED: "Confirmed",
        STATUS_DELIVERING: "Delivering",
        STATUS_DONE: "Done",
    }

    user = ForeignKey(
        to=User,
        on_delete=CASCADE,
        related_name="orders",
    )
    restaurant = ForeignKey(
        to=Restaurant,
        on_delete=CASCADE,
        related_name="orders",
    )
    address = ForeignKey(
        to=Address,
        on_delete=SET_NULL,
        null=True,
        related_name="orders",
    )
    status = PositiveIntegerField(
        default=STATUS_NEW,
        choices=STATUS_CHOICES,
    )
    subtotal = DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    discount_total = DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    total = DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk} — {self.user}"


class OrderItem(Model):
    """
    OrderItem database (table) model.
    """

    order = ForeignKey(to=Order, on_delete=CASCADE, related_name="items")
    menu_item = ForeignKey(to=MenuItem, on_delete=SET_NULL, null=True)
    item_name = CharField(max_length=200)
    item_price = DecimalField(max_digits=10, decimal_places=2)
    quantity = PositiveIntegerField(default=1)
    line_total = DecimalField(max_digits=10, decimal_places=2)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item_name} x{self.quantity}"


class OrderItemOption(Model):
    """
    OrderItemOption database (table) model.
    """

    order_item = ForeignKey(to=OrderItem, on_delete=CASCADE, related_name="options")
    option_name = CharField(max_length=100)
    price_delta = DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )

    def __str__(self):
        return f"{self.option_name} (+{self.price_delta})"


class OrderPromo(Model):
    """
    Through-table between Order and PromoCode.
    """

    order = ForeignKey(to=Order, on_delete=CASCADE)
    promo = ForeignKey(to=PromoCode, on_delete=CASCADE)
    applied_amount = DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["order", "promo"],
                name="unique_order_promo",
            ),
        ]

    def __str__(self):
        return f"{self.promo} on {self.order}"
