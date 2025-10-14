# Django modules
from django.db.models import (
    CharField,
    TextField,
    SlugField,
    ForeignKey,
    ManyToManyField,
    DecimalField,
    BooleanField,
    IntegerField,
    DateTimeField,
    UniqueConstraint,
    CASCADE,
)
from django.core.validators import MinValueValidator

# Project modules
from apps.abstracts.models import AbstractSoftDeletableModel


class Restaurant(AbstractSoftDeletableModel):
    """
    Restaurant database model.
    """

    NAME_MAX_LEN = 200

    name = CharField(max_length=NAME_MAX_LEN, db_index=True)
    slug = SlugField(max_length=NAME_MAX_LEN, unique=True, blank=True)
    address = CharField(max_length=255, blank=True, null=True)
    phone = CharField(max_length=50, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(AbstractSoftDeletableModel):
    """
    Category database model.
    """

    NAME_MAX_LEN = 100

    name = CharField(max_length=NAME_MAX_LEN)
    slug = SlugField(max_length=NAME_MAX_LEN, unique=True, blank=True)

    def __str__(self):
        return self.name


class Option(AbstractSoftDeletableModel):
    """
    Option (e.g., 'Extra cheese', 'Large') model.
    """

    NAME_MAX_LEN = 100

    name = CharField(max_length=NAME_MAX_LEN)
    slug = SlugField(max_length=NAME_MAX_LEN, blank=True)
    is_required = BooleanField(default=False)

    def __str__(self):
        return self.name


class MenuItem(AbstractSoftDeletableModel):
    """
    MenuItem database model.
    """

    NAME_MAX_LEN = 200

    restaurant = ForeignKey(to=Restaurant, on_delete=CASCADE, related_name="menu_items")
    name = CharField(max_length=NAME_MAX_LEN)
    slug = SlugField(max_length=NAME_MAX_LEN, blank=True)
    description = TextField(blank=True, default="")
    base_price = DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_available = BooleanField(default=True)
    options = ManyToManyField(to=Option, through="ItemOption", through_fields=("menuitem", "option"), related_name="menu_items", blank=True)
    categories = ManyToManyField(to=Category, through="ItemCategory", through_fields=("menuitem", "category"), related_name="menu_items", blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} — {self.restaurant.name}"


class ItemCategory(AbstractSoftDeletableModel):
    """
    Through-table between MenuItem and Category with position.
    """

    menuitem = ForeignKey(to=MenuItem, on_delete=CASCADE)
    category = ForeignKey(to=Category, on_delete=CASCADE)
    position = IntegerField(default=0)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["menuitem", "category"], name="unique_item_category"),
        ]

    def __str__(self):
        return f"{self.menuitem} in {self.category} ({self.position})"


class ItemOption(AbstractSoftDeletableModel):
    """
    Through-table between MenuItem and Option with price adjustment.
    """

    menuitem = ForeignKey(to=MenuItem, on_delete=CASCADE)
    option = ForeignKey(to=Option, on_delete=CASCADE)
    price_delta = DecimalField(max_digits=8, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    is_default = BooleanField(default=False)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["menuitem", "option"], name="unique_item_option"),
        ]

    def __str__(self):
        return f"{self.option} for {self.menuitem} (+{self.price_delta})"
