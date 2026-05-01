from django.contrib import admin
from .models import Category, Product, ContactMessage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    prepopulated_fields = {'slug': ('name',)}  # Kategori adını yazarken slug otomatik dolsun
    list_filter = ['is_active']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Listede görünecek sütunlar
    list_display = ['name', 'category', 'sku', 'wholesale_price', 'public_price', 'show_public_price', 'allow_whatsapp_order', 'stock_quantity', 'is_active']

    # Sağ tarafta çıkacak filtreleme seçenekleri
    list_filter = ['is_active', 'category', 'created_at']

    # Arama çubuğu (İsim ve stok koduna göre aranabilir)
    search_fields = ['name', 'sku']

    # Ürün detayına girmeden listede hızlıca değiştirilebilecek alanlar
    list_editable = ['wholesale_price', 'public_price', 'show_public_price', 'allow_whatsapp_order', 'stock_quantity', 'is_active']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'message']
    list_editable = ['is_read']


# products/admin.py
from .models import FAQ # FAQ modelini projene import etmeyi unutma

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_active')
    list_editable = ('order', 'is_active') # Admin listesinden direkt sırasını değiştirebilirsin
    search_fields = ('question', 'answer')
