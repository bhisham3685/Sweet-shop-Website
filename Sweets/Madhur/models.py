from django.db import models
from django.core.validators import MinValueValidator


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_kg = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    image_url = models.URLField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Preparing", "Preparing"),
        ("Out for delivery", "Out for delivery"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]
    order_number = models.CharField(max_length=14, unique=True, editable=False)
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField()
    city = models.CharField(max_length=80)
    pincode = models.CharField(max_length=10)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="orders")
    quantity_kg = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.25)])
    message = models.CharField(max_length=250, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.order_number:
            import secrets
            self.order_number = "MT" + secrets.token_hex(5).upper()
        if self.product_id and self.quantity_kg:
            self.total_amount = self.product.price_per_kg * self.quantity_kg
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_number} - {self.customer_name}"
