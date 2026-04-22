from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q  # Arama işlemi için eklendi
from .models import Category, Product


@login_required(login_url='/login/')
def b2b_product_list(request):
    products = Product.objects.filter(is_active=True).select_related('category')
    categories = Category.objects.filter(is_active=True)

    # 1. URL'den gelen parametreleri al
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    sort_by = request.GET.get('sort', 'newest')  # Varsayılan sıralama: En yeniler

    # 2. Arama Filtresi (Hem isme hem stok koduna göre)
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(sku__icontains=query)
        )

    # 3. Kategori Filtresi
    if category_id:
        products = products.filter(category_id=category_id)

    # 4. Sıralama İşlemi
    if sort_by == 'price_asc':
        products = products.order_by('wholesale_price')
    elif sort_by == 'price_desc':
        products = products.order_by('-wholesale_price')
    elif sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')

    # Arama çubuğunda ve seçim kutularında kullanıcının eski seçimlerini tutmak için context'e yolluyoruz
    context = {
        'products': products,
        'categories': categories,
        'current_query': query,
        'current_category': category_id,
        'current_sort': sort_by,
    }

    return render(request, 'products/b2b_list.html', context)
