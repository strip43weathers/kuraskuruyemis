from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Product, ContactMessage, FAQ, Campaign, HeroSlide
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


    paginator = Paginator(products, 30)
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
        'current_sort': sort_by,
    }

    return render(request, 'products/b2b_list.html', context)


def public_product_list(request):
    """Fiyatların ve sepetin olmadığı halka açık katalog."""
    products = Product.objects.filter(is_active=True, is_public=True).select_related('category')
    categories = Category.objects.filter(is_active=True)
    campaigns = Campaign.objects.filter(is_active=True)

    hero_slides = HeroSlide.objects.filter(is_active=True).prefetch_related('products')

    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    sort_by = request.GET.get('sort', 'newest')
    campaign_id = request.GET.get('campaign', '')

    hero_id = request.GET.get('hero', '')

    if query:
        products = products.filter(Q(name__icontains=query) | Q(sku__icontains=query))

    if category_id:
        products = products.filter(category_id=category_id)

    if campaign_id:
        products = products.filter(campaigns__id=campaign_id)

    if hero_id:
        products = products.filter(hero_slides__id=hero_id)

    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    else:
        products = products.order_by('-created_at')

    paginator = Paginator(products, 15)
    page_number = request.GET.get('page')

    try:
        products_paginated = paginator.page(page_number)
    except PageNotAnInteger:
        products_paginated = paginator.page(1)
    except EmptyPage:
        products_paginated = paginator.page(paginator.num_pages)

    active_campaign = None
    if campaign_id:
        active_campaign = Campaign.objects.filter(id=campaign_id).first()

    active_hero = None
    if hero_id:
        active_hero = HeroSlide.objects.filter(id=hero_id).first()

    context = {
        'products': products_paginated,
        'categories': categories,
        'current_query': query,
        'current_category': category_id,
        'current_sort': sort_by,
        'current_campaign': campaign_id,
        'active_campaign': active_campaign,
        'current_hero': hero_id,
        'active_hero': active_hero,
        'campaigns': campaigns,
        'hero_slides': hero_slides,
    }

    return render(request, 'products/public_list.html', context)


def public_product_detail(request, pk):
    """Halka açık tekil ürün detay sayfası."""
    product = get_object_or_404(Product, pk=pk, is_active=True, is_public=True)
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
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message_text = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            phone=phone,
            email=email,
            message=message_text
        )

        messages.success(request, "Mesajınız başarıyla alındı. En kısa sürede size dönüş yapılacaktır.")
        return redirect('contact')

    return render(request, 'pages/contact.html', {'categories': categories})




