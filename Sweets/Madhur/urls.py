from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Madhur import views

urlpatterns = [
    path("", views.home, name="home"),
    path("sweets/", views.sweets, name="sweets"),
    path("gallery/", views.gallery, name="gallery"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("order/", views.place_order, name="place_order"),
    path("orders/", views.order_list, name="order_list"),
    path("track-order/", views.track_order, name="track_order"),
    path("order-success/<str:order_number>/", views.order_success, name="order_success"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
