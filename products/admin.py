# products/admin.py

from django.contrib import admin
from .models import Category, Product, ContactMessage, Campaign, FAQ, HeroSlide


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    prepopulated_fields = {'slug': ('name',)}  # Kategori adını yazarken slug otomatik dolsun
    list_filter = ['is_active']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Listede görünecek sütunlar
    list_display = ['name', 'category', 'sku', 'wholesale_price', 'unit_step', 'public_price', 'show_public_price', 'allow_whatsapp_order', 'stock_quantity', 'is_active']

    # Sağ tarafta çıkacak filtreleme seçenekleri
    list_filter = ['is_active', 'category', 'created_at']

    # Arama çubuğu (İsim ve stok koduna göre aranabilir)
    search_fields = ['name', 'sku']

    # Ürün detayına girmeden listede hızlıca değiştirilebilecek alanlar
    list_editable = ['wholesale_price', 'unit_step', 'public_price', 'show_public_price', 'allow_whatsapp_order', 'stock_quantity', 'is_active']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'message']
    list_editable = ['is_read']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_active')
    list_editable = ('order', 'is_active') # Admin listesinden direkt sırasını değiştirebilirsin
    search_fields = ('question', 'answer')



@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    # Ürünleri sağa-sola atarak kolayca seçmek için:
    filter_horizontal = ('products',)
    search_fields = ('title',)


# admin.py dosyasının en altındaki HeroSlideAdmin sınıfını BUNUNLA DEĞİŞTİR:

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    # 'product' yerine kendi yazdığımız 'get_products' fonksiyonunu çağırıyoruz
    list_display = ('title', 'get_products', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    filter_horizontal = ('products',)
    search_fields = ('title',)

    # Çoklu seçilen ürünleri aralarına virgül koyarak yan yana yazdırmak için özel fonksiyon:
    def get_products(self, obj):
        # Eğer çok fazla ürün seçilirse tablo taşmasın diye ilk 3'ünü gösterip sonuna ... koyabiliriz
        products = obj.products.all()
        if products.exists():
            return ", ".join([p.name for p in products[:3]]) + ("..." if products.count() > 3 else "")
        return "-"

    # Admin panelindeki sütun başlığının adı:
    get_products.short_description = "Seçili Ürünler"
