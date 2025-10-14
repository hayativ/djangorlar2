from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.catalogs.models import Restaurant, Category, Option, MenuItem, ItemCategory, ItemOption
from apps.commerces.models import Address, PromoCode, Order, OrderItem, OrderItemOption, OrderPromo
from django.utils import timezone
from random import randint, choice, sample
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = "Generate test data (≈20 records per model)."

    def handle(self, *args, **options):
        # Create some users
        users = []
        if User.objects.count() < 5:
            for i in range(5):
                u = User.objects.create_user(username=f"user{i+1}", email=f"user{i+1}@example.com", password="password123")
                users.append(u)
        else:
            users = list(User.objects.all()[:5])

        # Restaurants
        restaurants = []
        for i in range(5):
            r, _ = Restaurant.objects.get_or_create(slug=f"rest-{i+1}", defaults={"name": f"Restaurant {i+1}", "address": f"Addr {i+1}", "phone": f"100{i}"})
            restaurants.append(r)

        # Categories
        categories = []
        for i in range(5):
            c, _ = Category.objects.get_or_create(slug=f"cat-{i+1}", defaults={"name": f"Category {i+1}"})
            categories.append(c)

        # Options
        options = []
        for i in range(5):
            o, _ = Option.objects.get_or_create(slug=f"opt-{i+1}", defaults={"name": f"Option {i+1}"})
            options.append(o)

        # MenuItems
        menu_items = []
        for i in range(20):
            r = choice(restaurants)
            mi = MenuItem.objects.create(
                restaurant=r,
                name=f"Menu Item {i+1}",
                slug=f"menu-{i+1}",
                description="Delicious",
                base_price=Decimal(randint(5, 50)),
                is_available=True
            )
            menu_items.append(mi)
            # attach a category and an option
            ItemCategory.objects.create(menuitem=mi, category=choice(categories), position=randint(0, 10))
            ItemOption.objects.create(menuitem=mi, option=choice(options), price_delta=Decimal(randint(0, 5)), is_default=False)

        # Addresses (20 total)
        addresses = []
        for i in range(20):
            u = choice(users)
            a = Address.objects.create(user=u, street=f"Street {i+1}", city="City", postal_code=f"{10000+i}", country="Country")
            addresses.append(a)

        # Promo codes
        promo_codes = []
        for i in range(20):
            p = PromoCode.objects.create(code=f"PROMO{i+1:02d}", discount_percent=Decimal(randint(5, 30)), is_active=True)
            promo_codes.append(p)

        # Orders
        for i in range(20):
            u = choice(users)
            r = choice(restaurants)
            a = choice(addresses)
            order = Order.objects.create(user=u, restaurant=r, address=a, subtotal=Decimal("0.00"), discount_total=Decimal("0.00"), total=Decimal("0.00"))
            chosen_items = sample(menu_items, k=randint(1, 3))
            subtotal = Decimal("0.00")
            for mi in chosen_items:
                qty = randint(1, 3)
                price = mi.base_price
                line_total = price * qty
                OrderItem.objects.create(order=order, menu_item=mi, item_name=mi.name, item_price=price, quantity=qty, line_total=line_total)
                subtotal += line_total
            promo = choice(promo_codes)
            applied = (subtotal * promo.discount_percent / Decimal(100)).quantize(Decimal("0.01"))
            OrderPromo.objects.create(order=order, promo=promo, applied_amount=applied)
            order.subtotal = subtotal
            order.discount_total = applied
            order.total = subtotal - applied
            order.save()

        self.stdout.write(self.style.SUCCESS("Generated test data for catalogs and commerces."))
