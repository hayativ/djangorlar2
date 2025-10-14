from django.contrib import admin
from .models import Address, Order, OrderItem, OrderItemOption, PromoCode, OrderPromo

def soft_delete(modeladmin, request, queryset):
    for obj in queryset:
        obj.soft_delete()
soft_delete.short_description = "Soft delete selected"

def restore(modeladmin, request, queryset):
    for obj in queryset:
        obj.restore()
restore.short_description = "Restore selected"

def hard_delete(modeladmin, request, queryset):
    for obj in queryset:
        obj.hard_delete()
hard_delete.short_description = "Hard delete selected (irreversible)"


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "street", "city", "deleted_at")
    search_fields = ("street", "city")
    actions = [soft_delete, restore, hard_delete]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "restaurant", "address", "status", "total", "deleted_at")
    list_filter = ("status", "restaurant")
    search_fields = ("user__username", "restaurant__name")
    actions = [soft_delete, restore, hard_delete]
    inlines = []


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "item_name", "item_price", "quantity", "line_total")
    actions = [soft_delete, restore, hard_delete]


@admin.register(OrderItemOption)
class OrderItemOptionAdmin(admin.ModelAdmin):
    list_display = ("id", "order_item", "option_name", "price_delta")
    actions = [soft_delete, restore, hard_delete]


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "discount_percent", "is_active", "deleted_at")
    list_filter = ("is_active",)
    search_fields = ("code",)
    actions = [soft_delete, restore, hard_delete]


@admin.register(OrderPromo)
class OrderPromoAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "promo", "applied_amount")
    actions = [soft_delete, restore, hard_delete]
