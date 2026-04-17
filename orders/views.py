from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import transaction  # En kritik kütüphanemiz
from decimal import Decimal

from products.models import Product
from .models import Order, OrderItem
from .cart import Cart


@require_POST
@login_required(login_url='/login/')
def cart_add(request, product_id):
    """Form üzerinden gelen miktar (KG) ile sepete ürün ekler."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    # HTML formundan gelecek 'quantity' değerini alıyoruz
    quantity = request.POST.get('quantity')

    if quantity:
        cart.add(product=product, quantity=quantity)

    # Ürün eklendikten sonra sepet detay sayfasına yönlendir
    return redirect('orders:cart_detail')


@login_required(login_url='/login/')
def cart_detail(request):
    """Sepet içeriğini görüntüler."""
    cart = Cart(request)
    # Şablonu bir sonraki adımda oluşturacağız
    return render(request, 'orders/cart_detail.html', {'cart': cart})


@login_required(login_url='/login/')
def checkout(request):
    """Siparişi tamamlar ve stoktan güvenli bir şekilde düşer."""
    cart = Cart(request)

    if not cart.cart:
        messages.warning(request, "Sepetiniz boş. Lütfen ürün ekleyin.")
        return redirect('products:b2b_list')

    if request.method == 'POST':
        # Müşteri siparişi onayladı. transaction.atomic ile bu bloktaki işlemlerden
        # biri bile hata verirse (örneğin stok yetmezse) hiçbir şey veritabanına yazılmaz (rollback).
        try:
            with transaction.atomic():
                # 1. Sipariş kaydını oluştur
                order = Order.objects.create(
                    user=request.user,
                    status='RECEIVED',
                    order_note=request.POST.get('order_note', '')
                )

                total_amount = Decimal('0.00')

                # 2. Sepetteki ürünleri dön ve stok kontrolü yap
                for item_id, item_data in cart.cart.items():
                    # select_for_update(): Bu satırı okurken kilitler, başka bir işlem buraya müdahale edemez.
                    product = Product.objects.select_for_update().get(id=item_id)
                    quantity = Decimal(item_data['quantity'])
                    price = Decimal(item_data['price'])

                    # Stok kontrolü
                    if product.stock_quantity < quantity:
                        # Eğer stok yetersizse hata fırlat, transaction.atomic tüm süreci iptal etsin
                        raise ValueError(
                            f"{product.name} için yeterli stok yok! Kalan stok: {product.stock_quantity} kg")

                    # 3. Stoktan miktarı düş ve kaydet
                    product.stock_quantity -= quantity
                    product.save()

                    # 4. Sipariş kalemini oluştur
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        unit_price=price,
                        total_price=quantity * price
                    )

                    total_amount += (quantity * price)

                # 5. Toplam tutarı siparişe yaz
                order.total_amount = total_amount
                order.save()

                # 6. İşlem bitti, sepeti boşalt
                cart.clear()
                messages.success(request, f"Siparişiniz başarıyla alındı! Sipariş No: #{order.id}")

                # Başarılı olunca ürünler sayfasına geri dön
                return redirect('products:b2b_list')

        except ValueError as e:
            # Stok hatası mesajını müşteriye göster ve sepetine geri yolla
            messages.error(request, str(e))
            return redirect('orders:cart_detail')

        except Exception as e:
            # Beklenmeyen bir hata (veritabanı bağlantısı kopması vb.)
            messages.error(request, "Sipariş işlenirken bir hata oluştu. Lütfen tekrar deneyin.")
            return redirect('orders:cart_detail')

    # Eğer GET isteği ise, müşteriye sipariş öncesi "Onay" sayfasını göster
    return render(request, 'orders/checkout.html', {'cart': cart})
