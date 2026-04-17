from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Products ve Orders app'lerinin URL'lerini sisteme dahil ediyoruz
    path('urunler/', include('products.urls', namespace='products')),
    path('siparis/', include('orders.urls', namespace='orders')),
]
