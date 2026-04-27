from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200, verbose_name="Ürün Adı")
    sku = models.CharField(max_length=50, unique=True, verbose_name="Stok Kodu (SKU)")
    description = models.TextField(blank=True, verbose_name="Ürün Açıklaması")
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True, verbose_name="Ürün Görseli")

    # B2B için tek tip toptan fiyat
    wholesale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Toptan KG Fiyatı (TL)"
    )

    # Stok ve Minimum Sipariş - KG cinsinden olacağı için DecimalField
    stock_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Stok Miktarı (KG)"
    )
    minimum_order_quantity = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal('5.00'),  # Örn: Minimum 5 KG alınabilir
        validators=[MinValueValidator(Decimal('0.10'))],
        verbose_name="Minimum Sipariş Miktarı (KG)"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="1- Satışta mı? (Ana Şalter)",
        help_text="İşareti kaldırırsanız ürün sistemden tamamen gizlenir (Sezonu biten veya geçici olarak satışı durdurulan ürünler için kullanın)."
    )

    is_b2b = models.BooleanField(
        default=True,
        verbose_name="2- B2B Bayi Portalında Göster",
        help_text="Bu ürün, sisteme şifresiyle giriş yapan bayilerin sipariş ekranında (fiyatlarıyla birlikte) listelensin mi?"
    )

    is_public = models.BooleanField(
        default=True,
        verbose_name="3- Halka Açık Vitrinde Göster",
        help_text="Bu ürün, siteye dışarıdan giren normal ziyaretçilerin genel kataloğunda (fiyat görünmeden) sergilensin mi?"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"

    def __str__(self):
        return f"{self.name} ({self.stock_quantity} kg)"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ad Soyad")
    phone = models.CharField(max_length=20, verbose_name="Telefon Numarası")
    email = models.EmailField(verbose_name="E-Posta Adresi")
    message = models.TextField(verbose_name="Mesaj")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Gönderilme Tarihi")
    is_read = models.BooleanField(default=False, verbose_name="Okundu mu?")

    class Meta:
        verbose_name = "İletişim Mesajı"
        verbose_name_plural = "İletişim Mesajları"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email}"
