#Django modules
from django.contrib import 

#Project modules
from .models import (
    Address,
    Order,
    OrderItem,
    OrderItemOption,
    PromoCode,
    OrderPromo,
)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "city", "street")
    search_fields = ("city", "street")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "restaurant", "address", "status", "total")
    list_filter = ("status", "restaurant")
    search_fields = ("user__username", "restaurant__name")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "item_name", "item_price", "quantity", "line_total")
    list_filter = ("order",)


@admin.register(OrderItemOption)
class OrderItemOptionAdmin(admin.ModelAdmin):
    list_display = ("id", "order_item", "option_name", "price_delta")
    list_filter = ("order_item",)


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "discount_percent", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code",)


@admin.register(OrderPromo)
class OrderPromoAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "promo", "applied_amount")
    list_filter = ("promo",)
