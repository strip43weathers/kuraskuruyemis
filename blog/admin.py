from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on', 'is_active')
    list_filter = ('is_active', 'created_on')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)} # Başlığı yazarken slug otomatik dolar
