from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    # Sipariş statüleri
    STATUS_CHOICES = (
        ('RECEIVED', 'Sipariş Alındı'),
        ('PREPARING', 'Hazırlanıyor'),
        ('SHIPPED', 'Kargolandı / Teslimatta'),
        ('COMPLETED', 'Tamamlandı'),
        ('CANCELLED', 'İptal Edildi'),
    )

    # Siparişi veren müşteri (İleride custom user veya company modeline bağlanabilir)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='orders')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RECEIVED', verbose_name="Sipariş Durumu")
    order_note = models.TextField(blank=True, verbose_name="Müşteri Sipariş Notu")

    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Toplam Tutar")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sipariş"
        verbose_name_plural = "Siparişler"
        ordering = ['-created_at']

    def __str__(self):
        return f"Sipariş #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product,
                                on_delete=models.PROTECT)  # Ürün silinirse sipariş geçmişi bozulmasın diye PROTECT

    # Ağırlık bazlı alım
    quantity = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Miktar (KG)")

    # Sipariş anındaki fiyatı sabitlemek için (Ürün fiyatı sonradan değişirse geçmiş sipariş etkilenmesin)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Birim Fiyat (KG)")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Toplam Fiyat")

    def save(self, *args, **kwargs):
        # Kaydedilirken toplam fiyatı otomatik hesapla
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} kg {self.product.name}"