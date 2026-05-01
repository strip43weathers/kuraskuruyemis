from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField  # YENİ: CKEditor'ü içeri aktar


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Başlık")
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name="Blog Görseli")

    # ESKİ: content = models.TextField(verbose_name="İçerik")
    # YENİ: Artık RichTextField kullanıyoruz
    content = RichTextField(verbose_name="İçerik")

    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    is_active = models.BooleanField(default=True, verbose_name="Yayında mı?")

    class Meta:
        ordering = ['-created_on']
        verbose_name = "Blog Yazısı"
        verbose_name_plural = "Blog Yazıları"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])
