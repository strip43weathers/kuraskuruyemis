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

    is_active = models.BooleanField(default=True, verbose_name="Satışta mı?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"

    def __str__(self):
        return f"{self.name} ({self.stock_quantity} kg)"
