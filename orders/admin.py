from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    # Ürün seçerken açılır liste yerine ID tabanlı arama ekranı getirir (çok ürün olunca performansı kurtarır)
    raw_id_fields = ['product']
    extra = 0  # Fazladan boş satır gösterme
    readonly_fields = ['unit_price', 'total_price']  # Geçmiş siparişin fiyatı admin tarafından değiştirilemesin


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'id']

    # Siparişin içindeki kalemleri sayfaya dahil et
    inlines = [OrderItemInline]

    # Toplam tutar sepette otomatik hesaplandığı için adminde salt okunur yapıyoruz
    readonly_fields = ['total_amount']
