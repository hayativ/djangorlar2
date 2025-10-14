from django.contrib import admin
from .models import Restaurant, MenuItem, Category, ItemCategory, Option, ItemOption

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


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "deleted_at")
    search_fields = ("name",)
    actions = [soft_delete, restore, hard_delete]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "restaurant", "base_price", "is_available", "deleted_at")
    list_filter = ("restaurant", "is_available")
    search_fields = ("name",)
    actions = [soft_delete, restore, hard_delete]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "deleted_at")
    search_fields = ("name",)
    actions = [soft_delete, restore, hard_delete]


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "menuitem", "category", "position", "deleted_at")
    list_filter = ("category",)
    actions = [soft_delete, restore, hard_delete]


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_required", "deleted_at")
    search_fields = ("name",)
    actions = [soft_delete, restore, hard_delete]


@admin.register(ItemOption)
class ItemOptionAdmin(admin.ModelAdmin):
    list_display = ("id", "menuitem", "option", "price_delta", "is_default", "deleted_at")
    list_filter = ("is_default",)
    actions = [soft_delete, restore, hard_delete]
