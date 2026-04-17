from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Product

# B2B portalı olduğu için giriş yapmayanlar bu view'a erişemez
@login_required(login_url='/login/')
def b2b_product_list(request):
    # select_related ile kategorileri tek sorguda çekerek performansı artırıyoruz
    products = Product.objects.filter(is_active=True).select_related('category')
    categories = Category.objects.filter(is_active=True)

    context = {
        'products': products,
        'categories': categories,
    }
    # Bu şablonu bir sonraki adımda yazacağız
    return render(request, 'products/b2b_list.html', context)
