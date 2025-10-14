#Django modules
from django.contrib import admin

#Project modules
from .models import (
    Restaurant,
    MenuItem,
    Category,
    ItemCategory,
    Option,
    ItemOption,
)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "restaurant", "base_price", "is_available")
    list_filter = ("restaurant", "is_available")
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "menu_item", "category", "position")
    list_filter = ("category", "menu_item")


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(ItemOption)
class ItemOptionAdmin(admin.ModelAdmin):
    list_display = ("id", "menu_item", "option", "price_delta", "is_default")
    list_filter = ("menu_item", "is_default")
