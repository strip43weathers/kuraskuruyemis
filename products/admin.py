from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    prepopulated_fields = {'slug': ('name',)}  # Kategori adını yazarken slug otomatik dolsun
    list_filter = ['is_active']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Listede görünecek sütunlar
    list_display = ['name', 'category', 'sku', 'wholesale_price', 'stock_quantity', 'is_active']

    # Sağ tarafta çıkacak filtreleme seçenekleri
    list_filter = ['is_active', 'category', 'created_at']

    # Arama çubuğu (İsim ve stok koduna göre aranabilir)
    search_fields = ['name', 'sku']

    # Ürün detayına girmeden listede hızlıca değiştirilebilecek alanlar
    list_editable = ['wholesale_price', 'stock_quantity', 'is_active']
