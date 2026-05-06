from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # YENİ: Paginator sınıfları eklendi
from .models import Category, Product, ContactMessage
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import FAQ


@login_required(login_url='/login/')
def b2b_product_list(request):
    products = Product.objects.filter(is_active=True, is_b2b=True).select_related('category')
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
    paginator = Paginator(products, 40)
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
    sort_by = request.GET.get('sort', 'newest')  # YENİ: Sıralama parametresi

    # 1. Arama Filtresi
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(sku__icontains=query)
        )

    # 2. Kategori Filtresi
    if category_id:
        products = products.filter(category_id=category_id)

    # 3. YENİ: Sıralama İşlemi (Fiyatlar gizli olduğu için fiyata göre sıralama yok)
    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    else:
        products = products.order_by('-created_at')  # Varsayılan: En yeniler

    # 4. Sayfalama
    paginator = Paginator(products, 8)
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
        'current_sort': sort_by,  # YENİ: Seçilen sıralamayı şablona yolluyoruz
    }

    return render(request, 'products/public_list.html', context)


def public_product_detail(request, pk):
    """Halka açık tekil ürün detay sayfası."""
    # Sadece aktif ve vitrin için işaretlenmiş ürünü getir
    product = get_object_or_404(Product, pk=pk, is_active=True, is_public=True)
    # Menüdeki kategoriler için
    categories = Category.objects.filter(is_active=True)

    return render(request, 'products/public_detail.html', {
        'product': product,
        'categories': categories
    })


def about_us(request):
    """Hakkımızda Sayfası"""
    categories = Category.objects.filter(is_active=True)
    return render(request, 'pages/about.html', {'categories': categories})


def faq(request):
    faqs = FAQ.objects.filter(is_active=True)
    return render(request, 'pages/faq.html', {'faqs': faqs})


def contact(request):
    """İletişim ve Adres Sayfası"""
    categories = Category.objects.filter(is_active=True)

    if request.method == 'POST':
        # Formdaki 'name', 'phone', 'email' ve 'message' alanlarını yakala
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message_text = request.POST.get('message')

        # Veritabanına kaydet
        ContactMessage.objects.create(
            name=name,
            phone=phone,
            email=email,
            message=message_text
        )

        messages.success(request, "Mesajınız başarıyla alındı. En kısa sürede size dönüş yapılacaktır.")
        return redirect('contact')

    return render(request, 'pages/contact.html', {'categories': categories})




