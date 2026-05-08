# products/models.py

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
    image2 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True, verbose_name="Ürün Görseli 2")

    # B2B için tek tip toptan fiyat
    wholesale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Toptan KG Fiyatı (TL)"
    )
    public_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Vitrin/Perakende Fiyatı (TL)"
    )

    # YENİ EKLENEN: Vitrin Fiyatını Göster/Gizle Şalteri
    show_public_price = models.BooleanField(
        default=False,
        verbose_name="4- Vitrinde Fiyatı Göster",
        help_text="İşaretlenirse halka açık katalogda 'Vitrin/Perakende Fiyatı' görünür."
    )
    # models.py içindeki Product modeline şu alanı ekle:

    allow_whatsapp_order = models.BooleanField(
        default=True,
        verbose_name="5- WhatsApp Sipariş Butonu",
        help_text="Bu ürün için vitrinde 'WhatsApp ile Sipariş Ver' butonu görünsün mü?"
    )

    # Stok ve Minimum Sipariş - KG cinsinden olacağı için DecimalField
    stock_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Stok Miktarı (KG)"
    )

    unit_step = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('1.00'),
        validators=[MinValueValidator(Decimal('0.10'))],  # 0 veya eksi değer girilmesini engeller
        verbose_name="B2B Satış Katı (kg)",
        help_text="Bu ürünün kaçar kg'lık katlarla satılacağını serbestçe yazabilirsiniz. Hangi sayıyı girerseniz ürün o şekilde artar. Örneğin 2.5 girerseniz 2.5, 5, 7.5 10 şeklinde artar."
    )

    minimum_order_quantity = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.10'))],
        verbose_name="Minimum Sipariş Miktarı (KG)",
        help_text="Lütfen üst kısımdaki 'B2B Satış Katı' ile tam bölünebilen uyumlu bir rakam girin. Örneğin satış katı 2.5 ise buraya 2.5, 5, 7.5, 10 gibi değerler girin."
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


# products/models.py dosyasının en altına ekle

class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name="Soru")
    answer = models.TextField(verbose_name="Cevap")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıra", help_text="Küçük sayı önce gösterilir.")
    is_active = models.BooleanField(default=True, verbose_name="Yayında mı?")

    class Meta:
        ordering = ['order', '-id']
        verbose_name = "Sıkça Sorulan Soru"
        verbose_name_plural = "Sıkça Sorulan Sorular"

    def __str__(self):
        return self.question


# models.py dosyasının EN ALTINA ekleyin

# models.py içindeki Campaign modelini şu şekilde değiştirin:

class Campaign(models.Model):
    title = models.CharField(max_length=150, verbose_name="Kampanya/Bölüm Başlığı", help_text="Örn: En Sevilen Ürünler")
    # Görsel opsiyonel olsun, eğer sadece başlık ve ürünler görünsün istersen diye
    image = models.ImageField(upload_to='campaigns/%Y/%m/', verbose_name="Bölüm Banner Görseli (Opsiyonel)", blank=True,
                              null=True)

    # YENİ: Tek bir ürün yerine çoklu ürün seçimi
    products = models.ManyToManyField(Product, related_name='campaigns', verbose_name="Kampanyaya Dahil Ürünler")

    order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    is_active = models.BooleanField(default=True, verbose_name="Yayında mı?")

    class Meta:
        ordering = ['order', '-id']
        verbose_name = "Özel Bölüm / Kampanya"
        verbose_name_plural = "Özel Bölümler / Kampanyalar"

    def __str__(self):
        return self.title


class HeroSlide(models.Model):
    title = models.CharField(max_length=150, verbose_name="Slayt Başlığı (Sadece Admin Görür)")
    image = models.ImageField(upload_to='hero/%Y/%m/', verbose_name="Hero Görseli (Tavsiye: 1920x530)")

    # YENİ: Tek ürün yerine çoklu ürün seçimi
    products = models.ManyToManyField(
        Product,
        related_name='hero_slides',
        verbose_name="Yönlendirilecek Ürünler (Opsiyonel)",
        blank=True,
        help_text="Eğer ürün seçerseniz, slayta tıklandığında sayfa sadece o ürünleri listeleyecek şekilde filtrelenir."
    )

    order = models.PositiveIntegerField(default=0, verbose_name="Sıralama")
    is_active = models.BooleanField(default=True, verbose_name="Yayında mı?")

    class Meta:
        ordering = ['order', '-id']
        verbose_name = "Hero Slaytı"
        verbose_name_plural = "Hero Slaytları"

    def __str__(self):
        return self.title
