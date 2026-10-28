from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "customer_name", "phone", "email", "address", "city", "pincode",
            "product", "quantity_kg", "message",
        ]
        widgets = {
            "customer_name": forms.TextInput(attrs={"placeholder": "Your full name"}),
            "phone": forms.TextInput(attrs={"placeholder": "10-digit mobile number", "inputmode": "tel"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email (optional)"}),
            "address": forms.Textarea(attrs={"placeholder": "House number, street, area", "rows": 3}),
            "city": forms.TextInput(attrs={"placeholder": "City"}),
            "pincode": forms.TextInput(attrs={"placeholder": "PIN code"}),
            "quantity_kg": forms.NumberInput(attrs={"min": "0.25", "step": "0.25"}),
            "message": forms.TextInput(attrs={"placeholder": "Any special instruction (optional)"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product"].queryset = self.fields["product"].queryset.filter(is_available=True)
