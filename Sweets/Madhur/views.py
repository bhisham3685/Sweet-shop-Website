from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Product, Order
from .forms import OrderForm


STARTER_PRODUCTS = [
    {
        "name": "Gulab Jamun",
        "description": "Soft, warm and syrup-soaked classic mithai.",
        "price_per_kg": "250.00",
        "image_url": "/static/shop/img/Gulab_jamun.jpeg",
    },
    {
        "name": "Rasgulla",
        "description": "Light, spongy chenna balls in sweet syrup.",
        "price_per_kg": "220.00",
        "image_url": "/static/shop/img/Rasgulla.jpeg",
    },
    {
        "name": "Motichoor Laddu",
        "description": "Festive orange laddus, made for sharing.",
        "price_per_kg": "300.00",
        "image_url": "/static/shop/img/Motichoor_laddu.jpeg",
    },
    {
        "name": "Kaju Katli",
        "description": "Smooth cashew sweet with a delicate finish.",
        "price_per_kg": "700.00",
        "image_url": "/static/shop/img/Kaju_katli.jpeg",
    },
    {
        "name": "Jalebi",
        "description": "Crispy, golden spirals with a juicy centre.",
        "price_per_kg": "200.00",
        "image_url": "/static/shop/img/Jalebi.jpeg",
    },
    {
        "name": "Peda",
        "description": "Traditional milk peda with a rich, creamy taste.",
        "price_per_kg": "360.00",
        "image_url": "/static/shop/img/Peda.jpeg",
    },
]


def get_products():
    if not Product.objects.exists():
        # Demo fallback cards only. Add real products in Django Admin for ordering.
        return [
            Product(id=i + 1, name=item["name"], description=item["description"],
                    price_per_kg=item["price_per_kg"], image_url=item["image_url"], is_available=True)
            for i, item in enumerate(STARTER_PRODUCTS)
        ]
    return Product.objects.filter(is_available=True)


def home(request):
    products = list(get_products())[:3]
    return render(request, "shop/home.html", {"products": products})


def sweets(request):
    query = request.GET.get("q", "").strip()
    products = get_products()
    if query:
        if isinstance(products, list):
            products = [p for p in products if query.lower() in p.name.lower()]
        else:
            products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, "shop/sweets.html", {"products": products, "query": query})


def gallery(request):
    return render(request, "shop/gallery.html", {"products": list(get_products())})


def about(request):
    return render(request, "shop/about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        message = request.POST.get("message", "").strip()
        if name and message:
            messages.success(request, "Thank you! Your message has been received in this demo.")
            return redirect("contact")
        messages.error(request, "Please enter your name and message.")
    return render(request, "shop/contact.html")


def place_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            messages.success(request, "Your order has been placed.")
            return redirect("order_success", order_number=order.order_number)
    else:
        form = OrderForm()
        product_id = request.GET.get("product")
        if product_id:
            form.fields["product"].initial = product_id
    return render(request, "shop/order.html", {"form": form})


def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, "shop/order_success.html", {"order": order})


def order_list(request):
    # Public demo list; in a real shop, protect this page behind staff/customer login.
    orders = Order.objects.all()[:100]
    return render(request, "shop/orders.html", {"orders": orders})


def track_order(request):
    order = None
    searched = False
    if request.method == "POST":
        searched = True
        number = request.POST.get("order_number", "").strip().upper()
        phone = request.POST.get("phone", "").strip()
        order = Order.objects.filter(order_number=number, phone=phone).first()
        if not order:
            messages.error(request, "Order not found. Check the order number and phone number.")
    return render(request, "shop/track_order.html", {"order": order, "searched": searched})
