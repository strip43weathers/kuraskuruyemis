from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    readonly_fields = ['unit_price', 'total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'id']

    inlines = [OrderItemInline]

    readonly_fields = ['total_amount']


admin.site.site_header = "Kuraş Kuruyemiş Yönetim Paneli"
admin.site.index_title = "Hoşgeldiniz"
