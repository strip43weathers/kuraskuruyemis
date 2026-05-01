# branches/models.py
from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=200, verbose_name="Şube Adı")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    image = models.ImageField(upload_to='branches/', blank=True, null=True, verbose_name="Şube Görseli")
    address = models.TextField(blank=True, null=True, verbose_name="Adres")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")
    maps_link = models.URLField(max_length=500, blank=True, null=True, verbose_name="Google Haritalar Linki")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Şube"
        verbose_name_plural = "Şubeler"
        ordering = ['name']

    def __str__(self):
        return self.name
