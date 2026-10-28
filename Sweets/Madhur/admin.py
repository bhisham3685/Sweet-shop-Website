from django.contrib import admin
from .models import Product, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price_per_kg", "is_available", "created_at")
    list_filter = ("is_available",)
    search_fields = ("name", "description")
    list_editable = ("price_per_kg", "is_available")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "customer_name",
        "phone",
        "product",
        "quantity_kg",
        "total_amount",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("order_number", "customer_name", "phone")
    list_editable = ("status",)
    readonly_fields = (
        "order_number",
        "total_amount",
        "created_at",
        "updated_at",
    )