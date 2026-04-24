from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # YENİ: Paginator sınıfları eklendi
from .models import Category, Product


@login_required(login_url='/login/')
def b2b_product_list(request):
    products = Product.objects.filter(is_active=True).select_related('category')
    categories = Category.objects.filter(is_active=True)

    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    sort_by = request.GET.get('sort', 'newest')

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(sku__icontains=query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    if sort_by == 'price_asc':
        products = products.order_by('wholesale_price')
    elif sort_by == 'price_desc':
        products = products.order_by('-wholesale_price')
    elif sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')

    # --- SAYFALAMA (PAGINATION) İŞLEMİ ---
    # Her sayfada kaç ürün gösterileceğini belirliyoruz (Örn: 12)
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')  # URL'den '?page=2' gibi sayfa numarasını al

    try:
        products_paginated = paginator.page(page_number)
    except PageNotAnInteger:
        # Eğer sayfa numarası tam sayı değilse veya boşsa ilk sayfayı göster
        products_paginated = paginator.page(1)
    except EmptyPage:
        # Eğer girilen sayfa numarası toplam sayfa sayısından büyükse son sayfayı göster
        products_paginated = paginator.page(paginator.num_pages)

    context = {
        'products': products_paginated,  # Artık tüm listeyi değil, sadece o sayfanın ürünlerini yolluyoruz
        'categories': categories,
        'current_query': query,
        'current_category': category_id,
        'current_sort': sort_by,
    }

    return render(request, 'products/b2b_list.html', context)


def public_product_list(request):
    """Fiyatların ve sepetin olmadığı halka açık katalog."""
    products = Product.objects.filter(is_active=True, is_public=True).select_related('category')
    categories = Category.objects.filter(is_active=True)

    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')

    if query:
        products = products.filter(Q(name__icontains=query) | Q(sku__icontains=query))
    if category_id:
        products = products.filter(category_id=category_id)

    products = products.order_by('-created_at')

    # Sayfalama
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    try:
        products_paginated = paginator.page(page_number)
    except PageNotAnInteger:
        products_paginated = paginator.page(1)
    except EmptyPage:
        products_paginated = paginator.page(paginator.num_pages)

    context = {
        'products': products_paginated,
        'categories': categories,
        'current_query': query,
        'current_category': category_id,
    }
    return render(request, 'products/public_list.html', context)
